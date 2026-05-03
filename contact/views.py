import logging
import json
from urllib.parse import quote

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import get_language, gettext as _
from django.views.generic import FormView
from django.conf import settings

import requests

from core.models import ContactPage, SiteSettings
from projects.models import Project

from .forms import ContactForm
from .models import ContactMessage

logger = logging.getLogger(__name__)


class ContactFormView(FormView):
    template_name = "contact-us.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact_form")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["site"] = SiteSettings.objects.first()
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["contact_page"] = ContactPage.objects.first()
        return ctx

    def form_valid(self, form):
        site = SiteSettings.objects.first()
        is_arabic = (get_language() or "").startswith("ar")
        phone = (form.cleaned_data.get("phone") or "").strip()
        project_ids = form.cleaned_data.get("project") or []
        selected_projects = [
            project
            for project in Project.objects.filter(pk__in=project_ids, is_active=True).only("title", "status")
            if project.effective_status_for_filters == Project.ProjectStatus.CURRENT
        ]
        project_titles = [p.title for p in selected_projects]
        projects_text = ", ".join(project_titles) if project_titles else (_("Unknown project"))
        message_text = (form.cleaned_data.get("message") or "").strip()

        send_wa_api = bool(getattr(site, "contact_send_whatsapp_api", True))

        ContactMessage.objects.create(
            name=form.cleaned_data["name"],
            email="whatsapp-only@local.invalid",
            phone=phone,
            subject=projects_text[:255],
            message=message_text,
            send_via=(
                ContactMessage.SendVia.WHATSAPP
                if send_wa_api
                else ContactMessage.SendVia.EMAIL
            ),
        )

        lines_body = [
            _("Name: %(name)s") % {"name": form.cleaned_data["name"]},
            _("Phone: %(phone)s") % {"phone": phone},
            (_("Projects: %(projects)s") if not is_arabic else "المشاريع: %(projects)s") % {"projects": projects_text},
        ]
        if message_text:
            lines_body.extend(["", _("Message: %(message)s") % {"message": message_text}])
        body = "\n".join(str(s) for s in lines_body)

        name_key = (getattr(site, "contact_external_name_key", "") or "full_name").strip()
        mobile_key = (getattr(site, "contact_external_mobile_key", "") or "mobile").strip()
        project_key = (getattr(site, "contact_external_project_key", "") or "client_17774678038301").strip()
        external_payload = {
            name_key: form.cleaned_data["name"],
            mobile_key: phone,
            project_key: projects_text,
            "message": message_text,
        }
        external_payload.update(self._parse_extra_external_json(site))

        whatsapp_payload = {
            "name": form.cleaned_data["name"],
            "phone": phone,
            "projects": project_titles,
            "projects_text": projects_text,
            "message": message_text,
            "body": body,
            "to": getattr(site, "whatsapp_digits", ""),
        }

        external_url = (
            getattr(site, "contact_external_webhook_url", "") if site else ""
        ) or settings.CONTACT_EXTERNAL_WEBHOOK_URL
        whatsapp_api_url = (
            getattr(site, "contact_whatsapp_api_url", "") if site else ""
        ) or settings.CONTACT_WHATSAPP_API_URL
        whatsapp_api_url = (whatsapp_api_url or "").strip()
        if not whatsapp_api_url:
            whatsapp_api_url = self.request.build_absolute_uri(
                reverse("contact_whatsapp_webhook")
            )

        wa_to = (whatsapp_payload.get("to") or "").strip()
        logger.info(
            "========== contact form outbound ==========\n"
            "[CRM] POST %s\n"
            "[CRM] payload:\n%s",
            external_url,
            json.dumps(external_payload, ensure_ascii=False, indent=2),
        )
        if send_wa_api:
            logger.info(
                "[WhatsApp] POST %s\n"
                "[WhatsApp] destination number (to): %s\n"
                "[WhatsApp] message body (body field):\n%s\n"
                "[WhatsApp] full JSON payload:\n%s\n"
                "===========================================",
                whatsapp_api_url,
                wa_to or "(not set — add WhatsApp number in Site settings)",
                body,
                json.dumps(whatsapp_payload, ensure_ascii=False, indent=2),
            )
        else:
            logger.info(
                "[WhatsApp] skipped — «Send contact form to WhatsApp API» is disabled "
                "(CRM-only mode in Site settings).\n"
                "==========================================="
            )

        external_ok = self._post_json(
            external_url,
            external_payload,
            headers=None,
            label="external webhook",
        )

        if send_wa_api:
            wa_headers = {
                "Authorization": f"Bearer {settings.CONTACT_WHATSAPP_API_TOKEN}",
            }
            whatsapp_ok = self._post_json(
                whatsapp_api_url,
                whatsapp_payload,
                headers=wa_headers or None,
                label="whatsapp api",
            )
        else:
            whatsapp_ok = True

        if external_ok and whatsapp_ok:
            messages.success(
                self.request,
                _("Your request has been sent successfully."),
            )
        elif external_ok or whatsapp_ok:
            messages.warning(
                self.request,
                _("Your request was sent partially. Please check integration settings."),
            )
        else:
            messages.error(
                self.request,
                _("Request could not be delivered. Please contact support."),
            )

        open_wa = bool(getattr(site, "contact_open_whatsapp_after_submit", False)) and send_wa_api
        if open_wa and site and site.whatsapp_digits and (external_ok or whatsapp_ok):
            wa_url = f"https://wa.me/{site.whatsapp_digits}?text={quote(body, safe='')}"
            return HttpResponseRedirect(wa_url)

        return super().form_valid(form)

    def _post_json(self, url, payload, headers=None, label="integration"):
        target = (url or "").strip()
        if not target:
            logger.warning("Contact form %s skipped: URL is not configured.", label)
            return False
        req_headers = {"Content-Type": "application/json"}
        if headers:
            req_headers.update(headers)
        try:
            response = requests.post(
                target,
                json=payload,
                headers=req_headers,
                timeout=12,
            )
            response.raise_for_status()
            return True
        except Exception as exc:  # noqa: BLE001
            logger.exception("Contact form %s send failed: %s", label, exc)
            return False

    def _parse_extra_external_json(self, site):
        raw = (getattr(site, "contact_external_extra_json", "") or "").strip() if site else ""
        if not raw:
            return {}
        try:
            data = json.loads(raw)
        except Exception:  # noqa: BLE001
            logger.warning("Invalid contact_external_extra_json: not valid JSON object.")
            return {}
        if not isinstance(data, dict):
            logger.warning("Invalid contact_external_extra_json: expected JSON object.")
            return {}
        return data

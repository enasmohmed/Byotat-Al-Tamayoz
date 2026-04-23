from urllib.parse import quote

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import get_language, gettext as _
from django.views.generic import FormView

from core.models import ContactPage, SiteSettings
from projects.models import Project

from .forms import ContactForm
from .models import ContactMessage


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
        selected_projects = list(
            Project.objects.filter(pk__in=project_ids, is_active=True, status=Project.ProjectStatus.CURRENT).only(
                "title"
            )
        )
        project_titles = [p.title for p in selected_projects]
        projects_text = ", ".join(project_titles) if project_titles else (_("Unknown project"))
        message_text = (form.cleaned_data.get("message") or "").strip()

        ContactMessage.objects.create(
            name=form.cleaned_data["name"],
            email="whatsapp-only@local.invalid",
            phone=phone,
            subject=projects_text[:255],
            message=message_text,
            send_via=ContactMessage.SendVia.WHATSAPP,
        )

        lines_body = [
            _("Name: %(name)s") % {"name": form.cleaned_data["name"]},
            _("Phone: %(phone)s") % {"phone": phone},
            (_("Projects: %(projects)s") if not is_arabic else "المشاريع: %(projects)s") % {"projects": projects_text},
        ]
        if message_text:
            lines_body.extend(["", _("Message: %(message)s") % {"message": message_text}])
        body = "\n".join(str(s) for s in lines_body)

        wa_url = ""
        if site and site.whatsapp_digits:
            wa_text = body
            wa_url = f"https://wa.me/{site.whatsapp_digits}?text={quote(wa_text, safe='')}"

        if wa_url:
            messages.success(
                self.request,
                _("Opening WhatsApp so you can send the message to the company."),
            )
            return HttpResponseRedirect(wa_url)

        messages.error(
            self.request,
            _("Company WhatsApp is not configured. Please contact support."),
        )
        return HttpResponseRedirect(self.get_success_url())

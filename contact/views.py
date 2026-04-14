from urllib.parse import quote

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
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
        project_options = []
        projects = (
            Project.objects.filter(
                is_active=True,
                status__in=[Project.ProjectStatus.CURRENT, Project.ProjectStatus.UNDER_CONSTRUCTION],
            )
            .only("id", "title", "status")
            .order_by("-id")
        )
        for project in projects:
            project_options.append(
                {
                    "id": str(project.pk),
                    "title": project.title,
                    "status": project.status,
                    "status_label": str(project.status_label_for_value(project.status)),
                }
            )
        ctx["project_options"] = project_options
        return ctx

    def form_valid(self, form):
        site = SiteSettings.objects.first()
        phone = (form.cleaned_data.get("phone") or "").strip()
        project_id = form.cleaned_data["project"]
        selected_project = Project.objects.filter(pk=project_id).first()
        project_title = selected_project.title if selected_project else _("Unknown project")
        selected_categories = []
        if form.cleaned_data.get("project_status_current"):
            selected_categories.append(_("Current"))
        if form.cleaned_data.get("project_status_under_construction"):
            selected_categories.append(_("Under construction"))
        categories_text = " / ".join(selected_categories) if selected_categories else "-"

        ContactMessage.objects.create(
            name=form.cleaned_data["name"],
            email="whatsapp-only@local.invalid",
            phone=phone,
            subject=project_title,
            message=form.cleaned_data["message"],
            send_via=ContactMessage.SendVia.WHATSAPP,
        )

        lines_body = [
            _("Name: %(name)s") % {"name": form.cleaned_data["name"]},
            _("Phone: %(phone)s") % {"phone": phone},
            _("Project: %(project)s") % {"project": project_title},
            _("Project categories: %(categories)s") % {"categories": categories_text},
            "",
            form.cleaned_data["message"],
        ]
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

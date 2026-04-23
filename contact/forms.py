from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

from core.models import SiteSettings
from projects.models import Project


class ContactForm(forms.Form):
    name = forms.CharField(
        label=_("Name"),
        max_length=255,
        widget=forms.TextInput(attrs={"class": "form-control", "autocomplete": "name", "required": True}),
    )
    phone = forms.CharField(
        label=_("Phone"),
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control", "autocomplete": "tel", "required": True}),
    )
    project = forms.MultipleChoiceField(
        label=_("Projects"),
        choices=(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
    )
    message = forms.CharField(
        label=_("Message"),
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 5}),
    )
    send_via_whatsapp = forms.BooleanField(
        label=_("Send"),
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    def __init__(self, *args, site=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.site = site if site is not None else SiteSettings.objects.first()
        self.is_arabic = (get_language() or "").startswith("ar")
        has_wa = bool(self.site and getattr(self.site, "whatsapp_digits", ""))

        if self.is_arabic:
            self.fields["project"].label = "المشاريع"
            self.fields["phone"].label = "رقم الجوال"
            self.fields["send_via_whatsapp"].label = "إرسال"

        self.fields["send_via_whatsapp"].initial = True
        if has_wa:
            self.fields["send_via_whatsapp"].widget = forms.HiddenInput()

        self.fields["project"].choices = self._project_choices()

    def _project_choices(self):
        choices = []
        projects = Project.objects.filter(
            is_active=True,
            status=Project.ProjectStatus.CURRENT,
        ).order_by("-id")
        for project in projects:
            choices.append((str(project.pk), project.title))
        return choices

    def clean(self):
        cleaned = super().clean()
        if not self.site:
            raise ValidationError(_("Site settings are missing. Please contact the administrator."))

        has_wa = bool(getattr(self.site, "whatsapp_digits", ""))
        selected_projects = cleaned.get("project") or []
        if not selected_projects:
            self.add_error(
                "project",
                "يرجى اختيار مشروع واحد على الأقل."
                if self.is_arabic
                else _("Please choose at least one project."),
            )
        else:
            valid_count = Project.objects.filter(
                pk__in=selected_projects,
                is_active=True,
                status=Project.ProjectStatus.CURRENT,
            ).count()
            if valid_count != len(set(selected_projects)):
                self.add_error(
                    "project",
                    "يرجى اختيار مشاريع حالية صالحة فقط."
                    if self.is_arabic
                    else _("Please choose valid current projects only."),
                )

        if not has_wa:
            raise ValidationError(
                _("Company WhatsApp is not configured. Please ask the administrator to set it in Site settings.")
            )
        cleaned["send_via_whatsapp"] = True
        return cleaned

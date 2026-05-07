from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

import re

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
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "autocomplete": "tel",
                "required": True,
                "inputmode": "tel",
                "dir": "ltr",
                "placeholder": "+9665XXXXXXXX",
            }
        ),
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
        projects = Project.objects.filter(is_active=True).order_by("-id")
        for project in projects:
            if project.effective_status_for_filters == Project.ProjectStatus.CURRENT:
                choices.append((str(project.pk), project.title))
        return choices

    def clean(self):
        cleaned = super().clean()
        if not self.site:
            raise ValidationError(_("Site settings are missing. Please contact the administrator."))

        send_wa_api = bool(getattr(self.site, "contact_send_whatsapp_api", True))
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
            valid_ids = {
                str(project.pk)
                for project in Project.objects.filter(pk__in=selected_projects, is_active=True)
                if project.effective_status_for_filters == Project.ProjectStatus.CURRENT
            }
            if len(valid_ids) != len(set(selected_projects)):
                self.add_error(
                    "project",
                    "يرجى اختيار مشاريع حالية صالحة فقط."
                    if self.is_arabic
                    else _("Please choose valid current projects only."),
                )

        if send_wa_api and not has_wa:
            raise ValidationError(
                _("Company WhatsApp is not configured. Please ask the administrator to set it in Site settings.")
            )
        cleaned["send_via_whatsapp"] = True
        return cleaned

    def clean_phone(self):
        """
        Normalize mobile numbers to Saudi E.164: +9665XXXXXXXX.
        Accepts common user inputs: +9665XXXXXXXX, 9665XXXXXXXX, 05XXXXXXXX, 5XXXXXXXX.
        """
        raw = (self.cleaned_data.get("phone") or "").strip()
        if not raw:
            raise ValidationError(_("This field is required."))

        # Keep digits and a single leading '+' (also accept 00 prefix).
        s = raw.strip()
        s = re.sub(r"[\s\-\(\)\.]+", "", s)
        if s.startswith("00"):
            s = "+" + s[2:]
        if s.startswith("+"):
            s = "+" + "".join(c for c in s[1:] if c.isdigit())
        else:
            s = "".join(c for c in s if c.isdigit())

        digits = "".join(c for c in s if c.isdigit())

        national = ""
        if s.startswith("+966") and digits.startswith("966"):
            national = digits[3:]
        elif digits.startswith("966"):
            national = digits[3:]
        elif digits.startswith("05"):
            national = digits[1:]  # drop the leading 0
        elif digits.startswith("5") and len(digits) == 9:
            national = digits

        # Saudi mobile numbers are 9 digits and start with 5.
        if not (len(national) == 9 and national.startswith("5")):
            raise ValidationError(
                "يرجى إدخال رقم جوال سعودي صحيح مثل +9665XXXXXXXX أو 05XXXXXXXX."
                if self.is_arabic
                else _("Please enter a valid Saudi mobile number like +9665XXXXXXXX or 05XXXXXXXX.")
            )

        return f"+966{national}"

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from core.models import SiteSettings


class ContactForm(forms.Form):
    name = forms.CharField(
        label=_("Name"),
        max_length=255,
        widget=forms.TextInput(attrs={"class": "form-control", "autocomplete": "name", "required": True}),
    )
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={"class": "form-control", "autocomplete": "email", "required": True}),
    )
    phone = forms.CharField(
        label=_("Phone"),
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control", "autocomplete": "tel", "required": True}),
    )
    subject = forms.CharField(
        label=_("Subject"),
        max_length=255,
        widget=forms.TextInput(attrs={"class": "form-control", "required": True}),
    )
    message = forms.CharField(
        label=_("Message"),
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 5, "required": True}),
    )
    send_via_email = forms.BooleanField(
        label=_("Via company email"),
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
    send_via_whatsapp = forms.BooleanField(
        label=_("Via company WhatsApp"),
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    def __init__(self, *args, site=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.site = site if site is not None else SiteSettings.objects.first()
        has_email = bool(self.site and (self.site.email or "").strip())
        has_wa = bool(self.site and getattr(self.site, "whatsapp_digits", ""))

        if has_email and has_wa:
            self.fields["send_via_email"].initial = True
            self.fields["send_via_whatsapp"].initial = True
        elif has_email:
            self.fields["send_via_email"].initial = True
            self.fields["send_via_whatsapp"].initial = False
            self.fields["send_via_whatsapp"].widget = forms.HiddenInput()
        elif has_wa:
            self.fields["send_via_email"].initial = False
            self.fields["send_via_whatsapp"].initial = True
            self.fields["send_via_email"].widget = forms.HiddenInput()
        else:
            self.fields["send_via_email"].initial = False
            self.fields["send_via_whatsapp"].initial = False

    def clean(self):
        cleaned = super().clean()
        if not self.site:
            raise ValidationError(_("Site settings are missing. Please contact the administrator."))

        has_email = bool((self.site.email or "").strip())
        has_wa = bool(getattr(self.site, "whatsapp_digits", ""))
        send_email = bool(cleaned.get("send_via_email"))
        send_wa = bool(cleaned.get("send_via_whatsapp"))

        if not send_email and not send_wa:
            raise ValidationError(_("Please choose at least one: email or WhatsApp."))

        if send_email and not has_email:
            raise ValidationError(
                _("Company email is not configured. Uncheck email or ask the administrator to set it in Site settings.")
            )
        if send_wa and not has_wa:
            raise ValidationError(
                _("Company WhatsApp is not configured. Uncheck WhatsApp or ask the administrator to set it in Site settings.")
            )
        return cleaned

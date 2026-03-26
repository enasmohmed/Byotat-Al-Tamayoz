from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from core.models import SiteSettings

from .models import ContactMessage


class ContactForm(forms.Form):
    name = forms.CharField(
        label=_("Name"),
        max_length=255,
        widget=forms.TextInput(attrs={"class": "form-control", "autocomplete": "name"}),
    )
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={"class": "form-control", "autocomplete": "email"}),
    )
    phone = forms.CharField(
        label=_("Phone (optional)"),
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "autocomplete": "tel"}),
    )
    subject = forms.CharField(
        label=_("Subject"),
        max_length=255,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    message = forms.CharField(
        label=_("Message"),
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 5}),
    )
    send_via = forms.ChoiceField(
        label=_("Send message via"),
        choices=ContactMessage.SendVia.choices,
        widget=forms.RadioSelect(attrs={"class": "contact-send-via"}),
        initial=ContactMessage.SendVia.EMAIL,
    )

    def __init__(self, *args, site=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.site = site if site is not None else SiteSettings.objects.first()
        choices = []
        if self.site and (self.site.email or "").strip():
            choices.append((ContactMessage.SendVia.EMAIL, _("Via company email")))
        if self.site and getattr(self.site, "whatsapp_digits", ""):
            choices.append((ContactMessage.SendVia.WHATSAPP, _("Via company WhatsApp")))

        fld = self.fields["send_via"]
        fld.help_text = ""

        if not choices:
            fld.choices = [
                (ContactMessage.SendVia.EMAIL, _("Via company email")),
                (ContactMessage.SendVia.WHATSAPP, _("Via company WhatsApp")),
            ]
        else:
            fld.choices = choices
            if len(choices) == 1:
                only = choices[0][0]
                fld.initial = only
                fld.widget = forms.HiddenInput()
                fld.choices = choices

    def clean(self):
        cleaned = super().clean()
        send_via = cleaned.get("send_via")
        if not self.site:
            raise ValidationError(_("Site settings are missing. Please contact the administrator."))
        if send_via == ContactMessage.SendVia.EMAIL:
            if not (self.site.email or "").strip():
                raise ValidationError(
                    _("Company email is not configured. Choose WhatsApp or ask the administrator to set it in Site settings.")
                )
        elif send_via == ContactMessage.SendVia.WHATSAPP:
            if not getattr(self.site, "whatsapp_digits", ""):
                raise ValidationError(
                    _("Company WhatsApp is not configured. Choose email or ask the administrator to set it in Site settings.")
                )
        return cleaned

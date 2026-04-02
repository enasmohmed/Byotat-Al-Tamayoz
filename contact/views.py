from urllib.parse import quote

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import FormView

from core.models import ContactPage, SiteSettings

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
        send_email = bool(form.cleaned_data.get("send_via_email"))
        send_wa = bool(form.cleaned_data.get("send_via_whatsapp"))
        subject = form.cleaned_data["subject"].strip()
        phone = (form.cleaned_data.get("phone") or "").strip()

        if send_email and send_wa:
            send_via = ContactMessage.SendVia.BOTH
        elif send_wa:
            send_via = ContactMessage.SendVia.WHATSAPP
        else:
            send_via = ContactMessage.SendVia.EMAIL

        ContactMessage.objects.create(
            name=form.cleaned_data["name"],
            email=form.cleaned_data["email"],
            phone=phone,
            subject=subject,
            message=form.cleaned_data["message"],
            send_via=send_via,
        )

        lines_body = [
            _("Subject: %(subject)s") % {"subject": subject},
            _("Name: %(name)s") % {"name": form.cleaned_data["name"]},
            _("Email: %(email)s") % {"email": form.cleaned_data["email"]},
            _("Phone: %(phone)s") % {"phone": phone},
            "",
            form.cleaned_data["message"],
        ]
        body = "\n".join(str(s) for s in lines_body)

        recipient = (site.email.strip() if site and site.email else "") or ""

        if send_email and recipient:
            send_mail(
                subject=f"[{_('Contact')}] {subject}",
                message=body,
                from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None) or recipient,
                recipient_list=[recipient],
                fail_silently=True,
            )

        wa_url = None
        if send_wa and site and site.whatsapp_digits:
            wa_lines = [
                f"*{_('Subject')}:* {subject}",
                f"*{_('Name')}:* {form.cleaned_data['name']}",
                f"*{_('Email')}:* {form.cleaned_data['email']}",
                f"*{_('Phone')}:* {phone}",
                "",
                form.cleaned_data["message"],
            ]
            wa_text = "\n".join(wa_lines)
            wa_url = f"https://wa.me/{site.whatsapp_digits}?text={quote(wa_text, safe='')}"

        if send_wa and wa_url:
            if send_email and recipient:
                messages.success(
                    self.request,
                    _("Your message was sent by email. Opening WhatsApp so you can send the same message there too."),
                )
            else:
                messages.success(
                    self.request,
                    _("Opening WhatsApp so you can send the message to the company."),
                )
            return HttpResponseRedirect(wa_url)

        messages.success(
            self.request,
            _("Thank you! Your message has been sent. We will get back to you soon."),
        )
        return super().form_valid(form)

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
        send_via = form.cleaned_data["send_via"]
        subject = form.cleaned_data["subject"].strip()

        ContactMessage.objects.create(
            name=form.cleaned_data["name"],
            email=form.cleaned_data["email"],
            phone=(form.cleaned_data.get("phone") or "").strip(),
            subject=subject,
            message=form.cleaned_data["message"],
            send_via=send_via,
        )

        if send_via == ContactMessage.SendVia.WHATSAPP:
            phone = (form.cleaned_data.get("phone") or "").strip()
            lines = [
                f"*{_('Subject')}:* {subject}",
                f"*{_('Name')}:* {form.cleaned_data['name']}",
                f"*{_('Email')}:* {form.cleaned_data['email']}",
            ]
            if phone:
                lines.append(f"*{_('Phone')}:* {phone}")
            lines.append("")
            lines.append(form.cleaned_data["message"])
            text = "\n".join(lines)
            safe = quote(text, safe="")
            url = f"https://wa.me/{site.whatsapp_digits}?text={safe}"
            messages.success(
                self.request,
                _("Opening WhatsApp so you can send the message to the company."),
            )
            return HttpResponseRedirect(url)

        recipient = (site.email.strip() if site and site.email else "") or ""
        if recipient:
            lines = [
                _("Subject: %(subject)s") % {"subject": subject},
                _("Name: %(name)s") % {"name": form.cleaned_data["name"]},
                _("Email: %(email)s") % {"email": form.cleaned_data["email"]},
            ]
            phone = (form.cleaned_data.get("phone") or "").strip()
            if phone:
                lines.append(_("Phone: %(phone)s") % {"phone": phone})
            lines.append("")
            lines.append(form.cleaned_data["message"])
            body = "\n".join(str(s) for s in lines)

            send_mail(
                subject=f"[{_('Contact')}] {subject}",
                message=body,
                from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None) or recipient,
                recipient_list=[recipient],
                fail_silently=True,
            )

        messages.success(
            self.request,
            _("Thank you! Your message has been sent. We will get back to you soon."),
        )
        return super().form_valid(form)

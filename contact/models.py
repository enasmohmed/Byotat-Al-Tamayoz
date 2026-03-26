from django.db import models
from django.utils.translation import gettext_lazy as _


class ContactMessage(models.Model):
    class SendVia(models.TextChoices):
        EMAIL = "email", _("Company email")
        WHATSAPP = "whatsapp", _("Company WhatsApp")

    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True, default="")
    subject = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField()
    send_via = models.CharField(
        max_length=16,
        choices=SendVia.choices,
        default=SendVia.EMAIL,
        verbose_name=_("Send via"),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.email}"

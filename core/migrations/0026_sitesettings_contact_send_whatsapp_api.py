from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0025_sitesettings_disable_wa_browser_redirect"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="contact_send_whatsapp_api",
            field=models.BooleanField(
                default=True,
                help_text="Uncheck to send the form only to the CRM/webhook. WhatsApp API calls are skipped; the WhatsApp number field below is then optional (still used for footer/chat links if filled).",
                verbose_name="Send contact form to WhatsApp API",
            ),
        ),
    ]

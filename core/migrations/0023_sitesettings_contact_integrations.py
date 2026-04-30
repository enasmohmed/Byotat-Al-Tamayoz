from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0022_footersettings_fal_license_logo"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="contact_external_webhook_url",
            field=models.URLField(
                blank=True,
                help_text="Receives contact form data as JSON (CRM/webhook integration).",
                null=True,
                verbose_name="Contact external webhook URL",
            ),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="contact_open_whatsapp_after_submit",
            field=models.BooleanField(
                default=False,
                help_text="If enabled, after API send succeeds the browser opens WhatsApp with the same prefilled message.",
                verbose_name="Open WhatsApp after submit",
            ),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="contact_whatsapp_api_url",
            field=models.URLField(
                blank=True,
                help_text="Server-to-server endpoint used to send WhatsApp messages automatically.",
                null=True,
                verbose_name="Contact WhatsApp API URL",
            ),
        ),
    ]

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0023_sitesettings_contact_integrations"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="contact_external_extra_json",
            field=models.TextField(
                blank=True,
                default="",
                help_text='Optional JSON object merged into payload. Example: {"source":"website","lang":"ar"}',
                verbose_name="External extra JSON fields",
            ),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="contact_external_mobile_key",
            field=models.CharField(
                blank=True,
                default="mobile",
                help_text="JSON key name used for contact phone in external webhook payload.",
                max_length=120,
                verbose_name="External key for mobile",
            ),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="contact_external_name_key",
            field=models.CharField(
                blank=True,
                default="full_name",
                help_text="JSON key name used for contact name in external webhook payload.",
                max_length=120,
                verbose_name="External key for name",
            ),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="contact_external_project_key",
            field=models.CharField(
                blank=True,
                default="client_17774678038301",
                help_text="JSON key name used for selected project title(s) in external webhook payload.",
                max_length=120,
                verbose_name="External key for project",
            ),
        ),
    ]

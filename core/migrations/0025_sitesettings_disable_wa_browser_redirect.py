from django.db import migrations


def disable_whatsapp_browser_redirect(apps, schema_editor):
    SiteSettings = apps.get_model("core", "SiteSettings")
    SiteSettings.objects.filter(contact_open_whatsapp_after_submit=True).update(
        contact_open_whatsapp_after_submit=False
    )


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0024_sitesettings_external_payload_keys"),
    ]

    operations = [
        migrations.RunPython(disable_whatsapp_browser_redirect, migrations.RunPython.noop),
    ]

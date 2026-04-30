from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0021_footersettings_snapchat_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="footersettings",
            name="fal_license_logo",
            field=models.ImageField(
                blank=True,
                help_text="Optional logo shown next to the Fal license number in the footer.",
                null=True,
                upload_to="footer/",
                verbose_name="Fal license logo",
            ),
        ),
    ]

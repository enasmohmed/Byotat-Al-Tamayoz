from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0020_sitesettings_hero_background_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="footersettings",
            name="snapchat_url",
            field=models.URLField(blank=True, default="", verbose_name="Snapchat URL"),
        ),
    ]

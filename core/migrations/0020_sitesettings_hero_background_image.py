from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0019_sitesettings_hero_video_file"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="hero_background_image",
            field=models.ImageField(
                blank=True,
                help_text="Used when no hero video is uploaded. If empty, the default theme image is used.",
                null=True,
                upload_to="settings/hero/",
                verbose_name="Home hero background image",
            ),
        ),
    ]

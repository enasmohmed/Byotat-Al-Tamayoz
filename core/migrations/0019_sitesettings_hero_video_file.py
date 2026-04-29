from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0018_footersettings_fal_license_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="hero_video_file",
            field=models.FileField(
                blank=True,
                help_text="Upload MP4 video for the home hero background. If empty, the default theme video is used.",
                null=True,
                upload_to="settings/hero/",
                verbose_name="Home hero video file",
            ),
        ),
    ]

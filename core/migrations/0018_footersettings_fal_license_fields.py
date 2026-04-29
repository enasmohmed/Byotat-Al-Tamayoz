from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0017_footersettings_footer_side_logo"),
    ]

    operations = [
        migrations.AddField(
            model_name="footersettings",
            name="fal_license_label",
            field=models.CharField(
                blank=True,
                default="",
                help_text='Example: "Fal License No." / "رقم رخصة فال"',
                max_length=120,
                verbose_name="Fal license label",
            ),
        ),
        migrations.AddField(
            model_name="footersettings",
            name="fal_license_label_ar",
            field=models.CharField(
                blank=True,
                default="",
                help_text='Example: "Fal License No." / "رقم رخصة فال"',
                max_length=120,
                null=True,
                verbose_name="Fal license label",
            ),
        ),
        migrations.AddField(
            model_name="footersettings",
            name="fal_license_label_en",
            field=models.CharField(
                blank=True,
                default="",
                help_text='Example: "Fal License No." / "رقم رخصة فال"',
                max_length=120,
                null=True,
                verbose_name="Fal license label",
            ),
        ),
        migrations.AddField(
            model_name="footersettings",
            name="fal_license_number",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Displayed below the side logo in the footer.",
                max_length=40,
                verbose_name="Fal license number",
            ),
        ),
    ]

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0016_alter_homecta_button_text_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="footersettings",
            name="footer_side_logo",
            field=models.ImageField(
                blank=True,
                help_text="Logo used in the last footer column. If empty, the main site logo is used.",
                null=True,
                upload_to="footer/",
                verbose_name="Footer side logo",
            ),
        ),
    ]

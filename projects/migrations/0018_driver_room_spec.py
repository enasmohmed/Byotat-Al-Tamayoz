# Manual migration: add has_driver_room specification flag

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0017_bathrooms_options_smart_control_warranty"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="has_driver_room",
            field=models.BooleanField(default=False, verbose_name="Driver room"),
        ),
    ]


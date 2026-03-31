# Generated manually for modeltranslation (en/ar)

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0015_allprojectspagesettings"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="rooms_options",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Optional. Shown in specs instead of a single count when units differ. Examples: «3، 4، 5» or «3 / 4 / 5».",
                max_length=120,
                verbose_name="Rooms — options text",
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="rooms_options_ar",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Optional. Shown in specs instead of a single count when units differ. Examples: «3، 4، 5» or «3 / 4 / 5».",
                max_length=120,
                null=True,
                verbose_name="Rooms — options text",
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="rooms_options_en",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Optional. Shown in specs instead of a single count when units differ. Examples: «3، 4، 5» or «3 / 4 / 5».",
                max_length=120,
                null=True,
                verbose_name="Rooms — options text",
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="room_count",
            field=models.PositiveSmallIntegerField(
                blank=True,
                help_text="Use when all units share one number. If rooms vary (e.g. 3, 4, 5), use «Rooms — options text» instead or as well.",
                null=True,
                verbose_name="Rooms count",
            ),
        ),
    ]

# Manual migration: bathrooms_options (i18n) + warranty_smart_control

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0016_project_rooms_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="bathrooms_options",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Optional. Shown in specs instead of a single count when units differ. Examples: «3، 4» or «2 / 3».",
                max_length=120,
                verbose_name="Bathrooms — options text",
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="bathrooms_options_ar",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Optional. Shown in specs instead of a single count when units differ. Examples: «3، 4» or «2 / 3».",
                max_length=120,
                null=True,
                verbose_name="Bathrooms — options text",
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="bathrooms_options_en",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Optional. Shown in specs instead of a single count when units differ. Examples: «3، 4» or «2 / 3».",
                max_length=120,
                null=True,
                verbose_name="Bathrooms — options text",
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="warranty_smart_control",
            field=models.CharField(
                blank=True,
                default="",
                help_text="e.g. years for smart home / building automation systems (التحكم الذكي).",
                max_length=120,
                verbose_name="Smart control warranty",
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="bathroom_count",
            field=models.PositiveSmallIntegerField(
                blank=True,
                help_text="Use when all units share one number. If bathrooms vary, use «Bathrooms — options text».",
                null=True,
                verbose_name="Bathrooms count",
            ),
        ),
    ]

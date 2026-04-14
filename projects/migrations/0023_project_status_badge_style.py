from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0022_project_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="project_status_badge_icon",
            field=models.CharField(
                blank=True,
                choices=[
                    ("", "Auto (from project status)"),
                    ("fa-crown", "Crown"),
                    ("fa-tools", "Tools"),
                    ("fa-check-circle", "Check circle"),
                    ("fa-hard-hat", "Hard hat"),
                    ("fa-key", "Key"),
                    ("fa-bolt", "Bolt"),
                    ("fa-award", "Award"),
                    ("fa-layer-group", "Layer group"),
                ],
                default="",
                help_text="Icon of the «Project status» badge. Leave empty to auto-match the selected status.",
                max_length=40,
                verbose_name="Project status badge icon",
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="project_status_badge_variant",
            field=models.CharField(
                blank=True,
                choices=[
                    ("", "Auto (from project status)"),
                    ("current", "Current style (gold)"),
                    ("under-construction", "Under construction style (green)"),
                    ("sold", "Sold style (red)"),
                    ("construction", "Construction style (amber)"),
                    ("available", "Available style (teal)"),
                    ("red", "Red style"),
                ],
                default="",
                help_text="Background style of the «Project status» badge. Leave empty to auto-match the selected status.",
                max_length=24,
                verbose_name="Project status badge style",
            ),
        ),
    ]

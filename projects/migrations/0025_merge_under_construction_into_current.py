from django.db import migrations, models


def move_under_construction_to_current(apps, schema_editor):
    Project = apps.get_model("projects", "Project")
    Project.objects.filter(status="under_construction").update(status="current")


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0024_alter_project_options_alter_projectcategory_options_and_more"),
    ]

    operations = [
        migrations.RunPython(move_under_construction_to_current, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="project",
            name="status",
            field=models.CharField(
                choices=[("current", "Current (الحالية)"), ("sold", "Sold (المباعة)")],
                db_index=True,
                default="current",
                help_text="Used for project filters and default status badge style.",
                max_length=24,
                verbose_name="Project status",
            ),
        ),
    ]

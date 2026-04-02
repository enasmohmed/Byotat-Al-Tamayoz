# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0004_bloglistpagesettings"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="display_date",
            field=models.DateField(
                blank=True,
                help_text=(
                    "Optional. Shown on the site like «Tuesday, 21 November 2023» or "
                    "«الثلاثاء، 21 نوفمبر 2023». If empty, the creation date is used."
                ),
                null=True,
                verbose_name="Display date",
            ),
        ),
    ]

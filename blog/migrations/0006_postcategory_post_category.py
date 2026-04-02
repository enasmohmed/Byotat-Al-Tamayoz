# Generated manually (modeltranslation fields for PostCategory.name)

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0005_post_display_date"),
    ]

    operations = [
        migrations.CreateModel(
            name="PostCategory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, verbose_name="Name")),
                ("name_ar", models.CharField(max_length=120, null=True, verbose_name="Name")),
                ("name_en", models.CharField(max_length=120, null=True, verbose_name="Name")),
                ("slug", models.SlugField(allow_unicode=True, blank=True, max_length=140, unique=True)),
            ],
            options={
                "verbose_name": "Post category",
                "verbose_name_plural": "Post categories",
                "ordering": ["name"],
            },
        ),
        migrations.AddField(
            model_name="post",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="posts",
                to="blog.postcategory",
                verbose_name="Category",
            ),
        ),
    ]

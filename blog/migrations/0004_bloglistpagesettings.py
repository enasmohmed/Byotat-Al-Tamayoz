# Generated manually — run makemigrations if your env differs.

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_default_language_ar'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogListPageSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hero_background', models.ImageField(blank=True, null=True, upload_to='blog/list_hero/', verbose_name='Hero background image')),
                ('hero_overlay', models.PositiveSmallIntegerField(default=7, help_text='1–10 (parallax overlay strength).', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='Hero overlay darkness')),
                ('hero_title_main', models.CharField(blank=True, default='', max_length=200, verbose_name='Page title (main)')),
                ('hero_title_main_ar', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='Page title (main)')),
                ('hero_title_main_en', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='Page title (main)')),
                ('hero_title_span', models.CharField(blank=True, default='', max_length=200, verbose_name='Page title (highlight span)')),
                ('hero_title_span_ar', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='Page title (highlight span)')),
                ('hero_title_span_en', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='Page title (highlight span)')),
                ('hero_intro', models.TextField(blank=True, default='', help_text='Optional short line under the page title (leave blank to hide).', verbose_name='Intro under title')),
                ('hero_intro_ar', models.TextField(blank=True, default='', help_text='Optional short line under the page title (leave blank to hide).', null=True, verbose_name='Intro under title')),
                ('hero_intro_en', models.TextField(blank=True, default='', help_text='Optional short line under the page title (leave blank to hide).', null=True, verbose_name='Intro under title')),
                ('breadcrumb_parent_label', models.CharField(blank=True, default='', help_text='Middle link (e.g. News). Leave blank for default translation.', max_length=120, verbose_name='Breadcrumb: parent link label')),
                ('breadcrumb_parent_label_ar', models.CharField(blank=True, default='', help_text='Middle link (e.g. News). Leave blank for default translation.', max_length=120, null=True, verbose_name='Breadcrumb: parent link label')),
                ('breadcrumb_parent_label_en', models.CharField(blank=True, default='', help_text='Middle link (e.g. News). Leave blank for default translation.', max_length=120, null=True, verbose_name='Breadcrumb: parent link label')),
                ('breadcrumb_current_label', models.CharField(blank=True, default='', help_text='Last crumb. Leave blank for default translation.', max_length=120, verbose_name='Breadcrumb: current page label')),
                ('breadcrumb_current_label_ar', models.CharField(blank=True, default='', help_text='Last crumb. Leave blank for default translation.', max_length=120, null=True, verbose_name='Breadcrumb: current page label')),
                ('breadcrumb_current_label_en', models.CharField(blank=True, default='', help_text='Last crumb. Leave blank for default translation.', max_length=120, null=True, verbose_name='Breadcrumb: current page label')),
            ],
            options={
                'verbose_name': 'News list page',
                'verbose_name_plural': 'News list page',
            },
        ),
    ]

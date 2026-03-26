from django.db import models
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _

# Create your models here.






class Page(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = RichTextField(blank=True, null=True)
    template_name = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    language = models.CharField(max_length=5, choices=[('en','English'), ('ar','Arabic')], default='en')

    def __str__(self):
        return f"{self.title} ({self.language})"

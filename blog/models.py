from django.db import models
from django.utils.text import slugify

# Create your models here.


from ckeditor.fields import RichTextField


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255, blank=True, allow_unicode=True)
    content = RichTextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    language = models.CharField(max_length=5, choices=[('en','English'), ('ar','Arabic')], default='ar')

    def _make_unique_slug(self, base: str) -> str:
        base = (base or '').strip('-')[:255] or 'post'
        slug = base
        n = 2
        qs = Post.objects.all()
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        while qs.filter(slug=slug).exists():
            suffix = f'-{n}'
            slug = f'{base[: 255 - len(suffix)]}{suffix}'
            n += 1
        return slug

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            raw = slugify(self.title, allow_unicode=True)
            self.slug = self._make_unique_slug(raw)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.language})"

from datetime import date

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField


class PostCategory(models.Model):
    name = models.CharField(max_length=120, verbose_name=_("Name"))
    slug = models.SlugField(max_length=140, unique=True, blank=True, allow_unicode=True)

    class Meta:
        ordering = ["name"]
        verbose_name = _("Post category")
        verbose_name_plural = _("Post categories")

    def _make_unique_slug(self, base: str) -> str:
        base = (base or "").strip("-")[:140] or "category"
        slug = base
        n = 2
        qs = PostCategory.objects.all()
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        while qs.filter(slug=slug).exists():
            suffix = f"-{n}"
            slug = f"{base[: 140 - len(suffix)]}{suffix}"
            n += 1
        return slug

    def save(self, *args, **kwargs):
        if not (self.slug or "").strip():
            raw = slugify((self.name or "").strip(), allow_unicode=True) or "category"
            self.slug = self._make_unique_slug(raw)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name or str(self.pk)


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255, blank=True, allow_unicode=True)
    content = RichTextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to="blog/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    display_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("Display date"),
        help_text=_(
            "Optional. Shown on the site like «Tuesday, 21 November 2023» or "
            "«الثلاثاء، 21 نوفمبر 2023». If empty, the creation date is used."
        ),
    )
    category = models.ForeignKey(
        PostCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
        verbose_name=_("Category"),
    )
    is_published = models.BooleanField(default=True)
    language = models.CharField(max_length=5, choices=[("en", "English"), ("ar", "Arabic")], default="ar")

    def _make_unique_slug(self, base: str) -> str:
        base = (base or "").strip("-")[:255] or "post"
        slug = base
        n = 2
        qs = Post.objects.all()
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        while qs.filter(slug=slug).exists():
            suffix = f"-{n}"
            slug = f"{base[: 255 - len(suffix)]}{suffix}"
            n += 1
        return slug

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            raw = slugify(self.title, allow_unicode=True)
            self.slug = self._make_unique_slug(raw)
        super().save(*args, **kwargs)

    @property
    def effective_display_date(self) -> date | None:
        """Calendar date used for public display (editorial date or created date)."""
        if self.display_date:
            return self.display_date
        if not self.created_at:
            return None
        dt = self.created_at
        if timezone.is_aware(dt):
            dt = timezone.localtime(dt)
        return dt.date()

    def __str__(self):
        return f"{self.title} ({self.language})"


class BlogListPageSettings(models.Model):
    """Hero + breadcrumb for /blog/ (single row in admin)."""

    hero_background = models.ImageField(
        upload_to="blog/list_hero/",
        blank=True,
        null=True,
        verbose_name=_("Hero background image"),
    )
    hero_overlay = models.PositiveSmallIntegerField(
        default=7,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name=_("Hero overlay darkness"),
        help_text=_("1–10 (parallax overlay strength)."),
    )
    hero_title_main = models.CharField(max_length=200, blank=True, default="", verbose_name=_("Page title (main)"))
    hero_title_span = models.CharField(max_length=200, blank=True, default="", verbose_name=_("Page title (highlight span)"))
    hero_intro = models.TextField(
        blank=True,
        default="",
        verbose_name=_("Intro under title"),
        help_text=_("Optional short line under the page title (leave blank to hide)."),
    )
    breadcrumb_parent_label = models.CharField(
        max_length=120,
        blank=True,
        default="",
        verbose_name=_("Breadcrumb: parent link label"),
        help_text=_("Middle link (e.g. News). Leave blank for default translation."),
    )
    breadcrumb_current_label = models.CharField(
        max_length=120,
        blank=True,
        default="",
        verbose_name=_("Breadcrumb: current page label"),
        help_text=_("Last crumb. Leave blank for default translation."),
    )

    class Meta:
        verbose_name = _("News list page")
        verbose_name_plural = _("News list page")

    def __str__(self):
        return str(_("News list page"))

from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField


class ProjectCategory(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, default="")
    default_language = models.CharField(max_length=5, choices=[("en", "English"), ("ar", "Arabic")], default="en")

    class Meta:
        verbose_name = _("Project Category")
        verbose_name_plural = _("Project Category")

    def __str__(self):
        return self.name or "Project Category"

    def _get_name_for_slug(self) -> str:
        """Choose best available name for slug generation (uses translated fields if title isn't set)."""
        raw = (self.name or "").strip()
        if raw:
            return raw
        raw = (getattr(self, "name_ar", "") or getattr(self, "name_en", "") or "").strip()
        return raw

    def _make_unique_slug(self, base_slug: str) -> str:
        base_slug = slugify(base_slug)
        if not base_slug:
            return ""

        slug = base_slug
        i = 1
        while ProjectCategory.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            i += 1
            slug = f"{base_slug}-{i}"
        return slug

    def save(self, *args, **kwargs):
        # Auto-generate slug from name (only when empty / not provided).
        if not (self.slug or "").strip():
            name_for_slug = self._get_name_for_slug()
            self.slug = self._make_unique_slug(name_for_slug) if name_for_slug else ""
        super().save(*args, **kwargs)


class Project(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, default="")
    description = RichTextField(blank=True, null=True)
    image = models.ImageField(upload_to="projects/", blank=True, null=True, verbose_name=_("Main cover image"))

    category = models.ForeignKey(
        ProjectCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="projects",
    )

    # موقع العرض (مترجم) + مفتاح تجميع للمشاريع المقترحة بنفس المنطقة
    city = models.CharField(
        max_length=120,
        blank=True,
        default="",
        verbose_name=_("City"),
        help_text=_('e.g. "Jeddah" / "جدة"'),
    )
    district = models.CharField(
        max_length=200,
        blank=True,
        default="",
        verbose_name=_("District / neighborhood"),
        help_text=_('e.g. "Al-Rawdah" / "حي الروضة"'),
    )
    area_key = models.SlugField(
        max_length=120,
        blank=True,
        default="",
        verbose_name=_("Area grouping key"),
        help_text=_(
            "Same value for all projects in one area (e.g. jeddah-rawdah). "
            "Used for «suggested in same area». Not shown on site."
        ),
    )

    area_sqm = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Area (m²) — single value"),
        help_text=_("Optional. Use area range below for min–max (e.g. 79.80–96)."),
    )
    area_sqm_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Area from (m²)"),
        help_text=_("Minimum unit area, e.g. 79.80"),
    )
    area_sqm_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Area to (m²)"),
        help_text=_("Maximum unit area, e.g. 96"),
    )
    room_count = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Rooms count"),
        help_text=_("Use when all units share one number. If rooms vary (e.g. 3, 4, 5), use «Rooms — options text» instead or as well."),
    )
    rooms_options = models.CharField(
        max_length=120,
        blank=True,
        default="",
        verbose_name=_("Rooms — options text"),
        help_text=_(
            "Optional. Shown in specs instead of a single count when units differ. "
            "Examples: «3، 4، 5» or «3 / 4 / 5»."
        ),
    )
    bathroom_count = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Bathrooms count"),
        help_text=_("Use when all units share one number. If bathrooms vary, use «Bathrooms — options text»."),
    )
    bathrooms_options = models.CharField(
        max_length=120,
        blank=True,
        default="",
        verbose_name=_("Bathrooms — options text"),
        help_text=_(
            "Optional. Shown in specs instead of a single count when units differ. "
            "Examples: «3، 4» or «2 / 3»."
        ),
    )
    has_living_hall = models.BooleanField(default=False, verbose_name=_("Has living hall (صالة)"))
    has_elevator = models.BooleanField(default=False, verbose_name=_("Has elevator"))
    has_private_parking = models.BooleanField(default=False, verbose_name=_("Private parking"))
    has_smart_home = models.BooleanField(default=False, verbose_name=_("Smart home"))
    has_maid_room = models.BooleanField(default=False, verbose_name=_("Maid room"))
    has_driver_room = models.BooleanField(default=False, verbose_name=_("Driver room"))

    promo_video = models.FileField(
        upload_to="projects/videos/",
        blank=True,
        null=True,
        verbose_name=_("Promo / walkthrough video"),
        help_text=_("Optional MP4 or WebM. A “Video” tab appears only when a file is uploaded."),
    )

    sold_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0"),
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_("Sold percentage"),
        help_text=_("0–100 (decimals allowed), for the progress ring."),
    )

    structural_warranty_years = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Structural warranty (years)"),
    )
    warranty_plumbing = models.CharField(max_length=120, blank=True, default="", verbose_name=_("Plumbing extensions warranty"))
    warranty_water_heaters = models.CharField(max_length=120, blank=True, default="", verbose_name=_("Water heaters warranty"))
    warranty_smart_control = models.CharField(
        max_length=120,
        blank=True,
        default="",
        verbose_name=_("Smart control warranty"),
        help_text=_("e.g. years for smart home / building automation systems (التحكم الذكي)."),
    )
    warranty_electrical_switches = models.CharField(max_length=120, blank=True, default="", verbose_name=_("Electrical switches warranty"))
    warranty_electrical_extensions = models.CharField(max_length=120, blank=True, default="", verbose_name=_("Electrical extensions warranty"))
    warranty_faucets = models.CharField(max_length=120, blank=True, default="", verbose_name=_("Faucets / mixers warranty"))
    warranty_lighting = models.CharField(max_length=120, blank=True, default="", verbose_name=_("Lighting warranty"))

    map_embed_url = models.TextField(
        blank=True,
        default="",
        verbose_name=_("Map embed URL"),
        help_text=_("Google Maps «Embed» iframe src URL (long paste OK)."),
    )

    is_active = models.BooleanField(default=True)
    default_language = models.CharField(max_length=5, choices=[("en", "English"), ("ar", "Arabic")], default="en")

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Project")

    def __str__(self):
        return self.title or "Project"

    def _get_title_for_slug(self) -> str:
        """Choose best available title for slug generation (uses translated fields if needed)."""
        raw = (self.title or "").strip()
        if raw:
            return raw
        raw = (getattr(self, "title_ar", "") or getattr(self, "title_en", "") or "").strip()
        return raw

    def _make_unique_slug(self, base_slug: str) -> str:
        base_slug = slugify(base_slug)
        if not base_slug:
            return ""

        slug = base_slug
        i = 1
        while Project.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            i += 1
            slug = f"{base_slug}-{i}"
        return slug

    def save(self, *args, **kwargs):
        # Auto-generate slug from title (only when empty / not provided).
        if not (self.slug or "").strip():
            title_for_slug = self._get_title_for_slug()
            self.slug = self._make_unique_slug(title_for_slug) if title_for_slug else ""
        super().save(*args, **kwargs)

    @property
    def location_line(self):
        """City | district for templates (uses translated fields)."""
        parts = [p.strip() for p in (self.city or "", self.district or "") if p and p.strip()]
        return " | ".join(parts) if parts else ""


class ProjectGalleryImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="gallery_images", verbose_name=_("Project"))
    image = models.ImageField(upload_to="projects/gallery/", verbose_name=_("Image"))
    sort_order = models.PositiveIntegerField(default=0, verbose_name=_("Sort order"))

    class Meta:
        verbose_name = _("Project gallery image")
        verbose_name_plural = _("Project gallery images")
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"{self.project_id} #{self.sort_order}"


class SectionTitle(models.Model):
    title = models.CharField(max_length=200)
    highlight = models.CharField(max_length=200)
    subtitle = models.TextField(blank=True, null=True)
    default_language = models.CharField(max_length=5, choices=[("en", "English"), ("ar", "Arabic")], default="ar")

    class Meta:
        verbose_name = _("Section Title")
        verbose_name_plural = _("Section Title")

    def __str__(self):
        return self.title or "Section Title"


class AllProjectsPageSettings(models.Model):
    """Hero + breadcrumb for the /projects/ listing (single row in admin)."""

    hero_background = models.ImageField(
        upload_to="projects/all_projects_hero/",
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
    breadcrumb_parent_label = models.CharField(
        max_length=120,
        blank=True,
        default="",
        verbose_name=_("Breadcrumb: projects link label"),
        help_text=_("Middle link. Leave blank for default translation."),
    )
    breadcrumb_current_label = models.CharField(
        max_length=120,
        blank=True,
        default="",
        verbose_name=_("Breadcrumb: current page label"),
        help_text=_("Last crumb. Leave blank for default translation."),
    )

    class Meta:
        verbose_name = _("All projects page")
        verbose_name_plural = _("All projects page")

    def __str__(self):
        return str(_("All projects page"))

import re

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField

class Service(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    short_description = models.CharField(max_length=255, blank=True, null=True)
    description = RichTextField(blank=True, null=True)
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    language = models.CharField(max_length=5, choices=[('en','English'), ('ar','Arabic')], default='en')

    def __str__(self):
        return f"{self.title} ({self.language})"

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")


class ServicePage(models.Model):
    """
    محتوى صفحة Service Page — سجل واحد (يُدار من الأدمن).
    """

    hero_background = models.ImageField(
        upload_to="service_page/hero/",
        blank=True,
        null=True,
        verbose_name=_("Hero background image"),
        help_text=_("Background for the page title (parallax)."),
    )
    hero_overlay = models.PositiveSmallIntegerField(
        default=7,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name=_("Hero overlay darkness"),
        help_text=_("0 = light, 10 = very dark (theme data-overlay)."),
    )
    hero_title_main = models.CharField(max_length=255, blank=True, default="", verbose_name=_("Hero title — first part"))
    hero_title_span = models.CharField(max_length=255, blank=True, default="", verbose_name=_("Hero title — highlighted part"))
    hero_breadcrumb_parent_label = models.CharField(
        max_length=120,
        blank=True,
        default="",
        verbose_name=_("Breadcrumb middle label"),
        help_text=_('e.g. "Pages" — appears between Home and current page.'),
    )

    gallery_image_1 = models.ImageField(upload_to="about_page/gallery/", blank=True, null=True, verbose_name=_("Gallery image 1"))
    gallery_image_2 = models.ImageField(upload_to="about_page/gallery/", blank=True, null=True, verbose_name=_("Gallery image 2"))
    gallery_image_3 = models.ImageField(upload_to="about_page/gallery/", blank=True, null=True, verbose_name=_("Gallery image 3"))
    gallery_image_4 = models.ImageField(upload_to="about_page/gallery/", blank=True, null=True, verbose_name=_("Gallery image 4"))

    intro_title_main = models.CharField(max_length=255, blank=True, default="", verbose_name=_("Intro title — first part"))
    intro_title_span = models.CharField(max_length=255, blank=True, default="", verbose_name=_("Intro title — highlighted part"))
    intro_lead = models.TextField(blank=True, default="", verbose_name=_("Intro lead paragraph"))
    intro_body = models.TextField(blank=True, default="", verbose_name=_("Intro body text"))
    intro_read_more_label = models.CharField(max_length=120, blank=True, default="", verbose_name=_("Read more button label"))
    intro_read_more_url = models.CharField(
        max_length=500,
        blank=True,
        default="",
        verbose_name=_("Read more URL"),
        help_text=_("e.g. /contact/ or full URL; leave empty to hide button."),
    )

    tab_mission_label = models.CharField(max_length=120, blank=True, default="", verbose_name=_("Tab: Mission label"))
    tab_vision_label = models.CharField(max_length=120, blank=True, default="", verbose_name=_("Tab: Vision label"))
    tab_values_label = models.CharField(max_length=120, blank=True, default="", verbose_name=_("Tab: Values label"))

    mission_image = models.ImageField(upload_to="about_page/tabs/", blank=True, null=True, verbose_name=_("Mission — image"))
    mission_heading_main = models.CharField(max_length=255, blank=True, default="", verbose_name=_("Mission — heading first part"))
    mission_heading_span = models.CharField(max_length=255, blank=True, default="", verbose_name=_("Mission — heading highlight"))
    mission_lead = models.TextField(blank=True, default="", verbose_name=_("Mission — lead"))
    mission_body = models.TextField(blank=True, default="", verbose_name=_("Mission — body"))

    vision_image = models.ImageField(upload_to="about_page/tabs/", blank=True, null=True, verbose_name=_("Vision — image"))
    vision_heading_main = models.CharField(max_length=255, blank=True, default="", verbose_name=_("Vision — heading first part"))
    vision_heading_span = models.CharField(max_length=255, blank=True, default="", verbose_name=_("Vision — heading highlight"))
    vision_lead = models.TextField(blank=True, default="", verbose_name=_("Vision — lead"))
    vision_body = models.TextField(blank=True, default="", verbose_name=_("Vision — body"))

    values_image = models.ImageField(upload_to="about_page/tabs/", blank=True, null=True, verbose_name=_("Values — image"))
    values_heading_main = models.CharField(max_length=255, blank=True, default="", verbose_name=_("Values — heading first part"))
    values_heading_span = models.CharField(max_length=255, blank=True, default="", verbose_name=_("Values — heading highlight"))
    values_lead = models.TextField(blank=True, default="", verbose_name=_("Values — lead"))
    values_body = models.TextField(blank=True, default="", verbose_name=_("Values — body"))

    policy_section_background = models.ImageField(
        upload_to="about_page/policy/",
        blank=True,
        null=True,
        verbose_name=_("Policy section — background"),
        help_text=_("Parallax background (optional)."),
    )
    policy_section_overlay = models.PositiveSmallIntegerField(
        default=9,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name=_("Policy section — overlay"),
        help_text=_("0–10, darker background behind text."),
    )
    policy_section_title_main = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name=_("Policy section — main title"),
        help_text=_("Large heading above the carousel (e.g. commitment / quality)."),
    )
    policy_section_title_span = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name=_("Policy section — highlighted title part"),
    )
    quality_policy_heading = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name=_("Quality policy — block title"),
        help_text=_('e.g. "Quality policy".'),
    )
    quality_policy_teaser = models.TextField(
        blank=True,
        default="",
        verbose_name=_("Quality policy — intro before bullets"),
        help_text=_("Optional short paragraph above the bullet list (teaser / lead-in)."),
    )
    quality_policy_points = models.TextField(
        blank=True,
        default="",
        verbose_name=_("Quality policy — bullet points"),
        help_text=_("One bullet per line."),
    )
    for_you_heading = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name=_('"For you" block — title'),
        help_text=_('e.g. "For you" / "من أجلكم".'),
    )
    for_you_body = models.TextField(
        blank=True,
        default="",
        verbose_name=_('"For you" block — text'),
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Services extended page")
        verbose_name_plural = _("Services extended page")

    def __str__(self):
        return str(_("Services extended page"))


class ServicesLanding(models.Model):
    """
    صفحة «خدماتنا» — سجل واحد: هيرو + عنوان جانبي للقسم الرمادي + بنود مع أيقونات.
    """

    hero_background = models.ImageField(
        upload_to="services/landing/hero/",
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
    hero_title_main = models.CharField(max_length=255, blank=True, default="", verbose_name=_("Hero title — main"))
    hero_title_span = models.CharField(max_length=255, blank=True, default="", verbose_name=_("Hero title — highlight"))
    breadcrumb_parent_label = models.CharField(
        max_length=120,
        blank=True,
        default="",
        verbose_name=_("Breadcrumb — middle link label"),
        help_text=_("Leave blank for default translation."),
    )
    breadcrumb_current_label = models.CharField(
        max_length=120,
        blank=True,
        default="",
        verbose_name=_("Breadcrumb — current page label"),
        help_text=_("Leave blank for default translation."),
    )
    sidebar_title_main = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name=_("Features block — title (main)"),
    )
    sidebar_title_span = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name=_("Features block — title (highlight)"),
    )
    sidebar_intro = models.TextField(blank=True, default="", verbose_name=_("Features block — intro under title"))
    section_pattern_image = models.ImageField(
        upload_to="services/landing/pattern/",
        blank=True,
        null=True,
        verbose_name=_("Grey section — pattern background (optional)"),
        help_text=_("Optional tile/pattern; leave empty to use theme default."),
    )

    class Meta:
        verbose_name = _("Our services page")
        verbose_name_plural = _("Our services page")

    def __str__(self):
        return str(_("Our services page"))


class ServicesFeature(models.Model):
    """بند في شبكة «لماذا نحن» / المميزات — أيقونة من فئة flaticon أو Font Awesome."""

    landing = models.ForeignKey(
        ServicesLanding,
        on_delete=models.CASCADE,
        related_name="features",
        verbose_name=_("Page"),
    )
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    description = models.TextField(blank=True, default="", verbose_name=_("Description"))
    icon_class = models.CharField(
        max_length=120,
        default="flaticon-innovation",
        verbose_name=_("Icon CSS classes"),
        help_text=_('Example: flaticon-innovation or "fas fa-cog". No angle brackets.'),
    )
    sort_order = models.PositiveSmallIntegerField(default=0, verbose_name=_("Sort order"))
    is_promoted = models.BooleanField(
        default=False,
        verbose_name=_("Show beside sidebar (large cell)"),
        help_text=_("At most one promoted item is shown next to the intro; others appear in the grid below."),
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))

    class Meta:
        ordering = ("sort_order", "id")
        verbose_name = _("Service feature item")
        verbose_name_plural = _("Service feature items")

    def __str__(self):
        return self.title or str(self.pk)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        raw = (self.icon_class or "").strip()
        if raw and not re.match(r"^[a-zA-Z0-9_\-\s]+$", raw):
            raise ValidationError(
                {"icon_class": _("Use only letters, numbers, spaces, hyphens and underscores (CSS class names).")}
            )


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
        verbose_name = _("About page")
        verbose_name_plural = _("About page")

    def __str__(self):
        return "About page"


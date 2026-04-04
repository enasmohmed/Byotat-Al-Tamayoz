import re

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ImageField(upload_to='settings/', blank=True, null=True)
    favicon = models.ImageField(upload_to='settings/', blank=True, null=True)
    primary_color = models.CharField(
        max_length=7,
        blank=True,
        null=True,
        verbose_name=_("Accent color"),
        help_text=_("Buttons, links, icons, progress bars, highlights — the color that should stand out."),
    )
    secondary_color = models.CharField(
        max_length=7,
        blank=True,
        null=True,
        verbose_name=_("Secondary accent"),
        help_text=_("Gradients with accent, secondary buttons, subtle accents."),
    )
    surface_color = models.CharField(
        max_length=7,
        blank=True,
        null=True,
        verbose_name=_("Surface / page background"),
        help_text=_("Main page background and light sections (e.g. #ececec)."),
    )
    dark_color = models.CharField(
        max_length=7,
        blank=True,
        null=True,
        verbose_name=_("Dark brand background"),
        help_text=_("Header (when fixed), footer, dark sections (e.g. #1d3338)."),
    )
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    whatsapp_number = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        verbose_name=_("WhatsApp number"),
        help_text=_("Digits only with country code, no spaces (e.g. 966501234567). Used for chat links."),
    )
    map_embed_url = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Google Maps embed URL"),
        help_text=_(
            "Paste the iframe src URL from Google Maps (Share → Embed a map). "
            "If empty, the contact page uses the default map from settings (e.g. Jeddah)."
        ),
    )
    default_language = models.CharField(max_length=5, choices=[('en','English'), ('ar','Arabic')], default='en')

    class Meta:
        verbose_name = _("Site Setting")
        verbose_name_plural = _("Site Settings")

    def __str__(self):
        return self.site_name or "Site Setting"

    @property
    def whatsapp_digits(self):
        """International number for https://wa.me/… (digits only)."""
        if not self.whatsapp_number:
            return ""
        return "".join(c for c in str(self.whatsapp_number) if c.isdigit())

    @property
    def whatsapp_link(self):
        """Full wa.me URL for side bar / templates (empty if no number)."""
        d = self.whatsapp_digits
        return f"https://wa.me/{d}" if d else ""

    @property
    def phone_call_link(self):
        """tel: href from Site settings phone (digits only when possible)."""
        if not self.phone:
            return ""
        raw = str(self.phone).strip()
        digits = re.sub(r"\D+", "", raw)
        if digits:
            return f"tel:{digits}"
        return f"tel:{raw}" if raw else ""


class HomeCTA(models.Model):
    text_main = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name=_("Main text"),
        help_text=_("Primary headline line on the home hero."),
    )
    text_highlight = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name=_("Highlighted text"),
        help_text=_("Optional second line or accent phrase (theme color). Leave empty if not used."),
    )
    button_text = models.CharField(
        max_length=120,
        blank=True,
        default="",
        verbose_name=_("Button text"),
        help_text=_("Label shown on the call-to-action button."),
    )
    button_url = models.CharField(
        max_length=500,
        blank=True,
        default="",
        verbose_name=_("Button URL"),
        help_text=_("Internal path like /contact/ or a full https:// URL."),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active"),
        help_text=_("When unchecked, this block is hidden on the home page."),
    )

    class Meta:
        verbose_name = _("Home CTA")
        verbose_name_plural = _("Home CTA")

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    def __str__(self):
        return str(_("Home CTA"))


class FooterSettings(models.Model):
    """
    إعدادات الفوتر (سجل واحد فقط — يُدار من الأدمن).
    """
    about_heading_main = models.CharField(
        max_length=120,
        blank=True,
        default="",
        verbose_name=_("About — first part of title"),
        help_text=_('Example: "About" in "About Us"'),
    )
    about_heading_span = models.CharField(
        max_length=120,
        blank=True,
        default="",
        verbose_name=_("About — colored part"),
        help_text=_('Example: "Us" (appears in theme color)'),
    )
    about_text = models.TextField(
        blank=True,
        default="",
        verbose_name=_("About — text"),
    )

    solutions_heading_main = models.CharField(
        max_length=120,
        blank=True,
        default="",
        verbose_name=_("Our Solutions — first part"),
        help_text=_('Example: "Our" in "Our Solutions"'),
    )
    solutions_heading_span = models.CharField(
        max_length=120,
        blank=True,
        default="",
        verbose_name=_("Our Solutions — colored part"),
        help_text=_('Example: "Solutions"'),
    )

    recent_heading_main = models.CharField(
        max_length=120,
        blank=True,
        default="",
        verbose_name=_("Recent Post — first part"),
        help_text=_('Example: "Recent" in "Recent Post"'),
    )
    recent_heading_span = models.CharField(
        max_length=120,
        blank=True,
        default="",
        verbose_name=_("Recent Post — colored part"),
        help_text=_('Example: "Post"'),
    )

    contact_heading_main = models.CharField(
        max_length=120,
        blank=True,
        default="",
        verbose_name=_("Get in touch — first part"),
        help_text=_('Example: "Get In"'),
    )
    contact_heading_span = models.CharField(
        max_length=120,
        blank=True,
        default="",
        verbose_name=_("Get in touch — colored part"),
        help_text=_('Example: "Touch"'),
    )

    address = models.TextField(
        blank=True,
        default="",
        verbose_name=_("Contact — address"),
    )
    phone = models.CharField(
        max_length=80,
        blank=True,
        default="",
        verbose_name=_("Contact — phone"),
        help_text=_(
            "Shown in the footer. Tap opens the dialer (tel:). You can use spaces or + for display; "
            "digits are used for the actual call link."
        ),
    )
    email = models.EmailField(
        blank=True,
        default="",
        verbose_name=_("Contact — email"),
    )

    footer_logo = models.ImageField(
        upload_to="footer/",
        blank=True,
        null=True,
        verbose_name=_("Footer logo"),
        help_text=_("If empty, the main site logo is used."),
    )

    hours_line1_label = models.CharField(
        max_length=120,
        blank=True,
        default="",
        verbose_name=_("Working hours — line 1 label"),
        help_text=_('Example: "Monday - Friday"'),
    )
    hours_line1_value = models.CharField(
        max_length=120,
        blank=True,
        default="",
        verbose_name=_("Working hours — line 1 hours"),
        help_text=_('Example: "10:00 to 6:00"'),
    )
    hours_line2_label = models.CharField(
        max_length=120,
        blank=True,
        default="",
        verbose_name=_("Working hours — line 2 label"),
    )
    hours_line2_value = models.CharField(
        max_length=120,
        blank=True,
        default="",
        verbose_name=_("Working hours — line 2 hours"),
    )

    facebook_url = models.URLField(blank=True, default="", verbose_name=_("Facebook URL"))
    twitter_url = models.URLField(blank=True, default="", verbose_name=_("X URL"))
    linkedin_url = models.URLField(blank=True, default="", verbose_name=_("LinkedIn URL"))
    instagram_url = models.URLField(blank=True, default="", verbose_name=_("Instagram URL"))
    youtube_url = models.URLField(blank=True, default="", verbose_name=_("YouTube URL"))

    copyright_suffix = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text=_("e.g. | All Rights Reserved"),
    )

    class Meta:
        verbose_name = _("Footer settings")
        verbose_name_plural = _("Footer settings")

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    def __str__(self):
        # لا تُرجَع gettext_lazy من __str__ — يسبب TypeError في الأدمن
        return str(_("Footer"))

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class FooterLink(models.Model):
    footer = models.ForeignKey(
        FooterSettings,
        on_delete=models.CASCADE,
        related_name="links",
    )
    title = models.CharField(max_length=255, verbose_name=_("Link title"))
    url = models.CharField(
        max_length=500,
        verbose_name=_("Link URL"),
        help_text=_("e.g. /blog/ or https://…"),
    )
    sort_order = models.PositiveIntegerField(default=0, verbose_name=_("Order"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))

    class Meta:
        verbose_name = _("Footer link")
        verbose_name_plural = _("Footer links")
        ordering = ("sort_order", "id")

    def __str__(self):
        return self.title or f"Link #{self.pk}"


class AboutPage(models.Model):
    """
    محتوى صفحة About Us — سجل واحد (يُدار من الأدمن).
    """

    hero_background = models.ImageField(
        upload_to="about_page/hero/",
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


class ContactPage(models.Model):
    """
    محتوى صفحة اتصل بنا — سجل واحد (يُدار من الأدمن).
    """

    hero_background = models.ImageField(
        upload_to="contact_page/hero/",
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
        help_text=_('e.g. "Contact" — appears between Home and current page title.'),
    )

    sidebar_title_main = models.CharField(max_length=255, blank=True, default="", verbose_name=_("Sidebar title — first part"))
    sidebar_title_span = models.CharField(max_length=255, blank=True, default="", verbose_name=_("Sidebar title — highlighted part"))
    sidebar_intro = models.TextField(
        blank=True,
        default="",
        verbose_name=_("Sidebar intro text"),
        help_text=_("Short paragraph next to contact details."),
    )

    form_heading_main = models.CharField(max_length=255, blank=True, default="", verbose_name=_("Form heading — first part"))
    form_heading_span = models.CharField(max_length=255, blank=True, default="", verbose_name=_("Form heading — highlighted part"))

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Contact page")
        verbose_name_plural = _("Contact page")

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    def __str__(self):
        return str(_("Contact page"))


class PartnerBrand(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True)
    logo = models.ImageField(upload_to='partners/', blank=False, null=False)
    website_url = models.URLField(blank=True, null=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Partner Brand")
        verbose_name_plural = _("Partner Brands")
        ordering = ("sort_order", "id")

    def __str__(self):
        return self.name or f"Partner #{self.pk}"

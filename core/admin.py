import core.translation  # noqa: F401 — تسجيل حقول modeltranslation

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline

from .models import AboutPage, ContactPage, FooterLink, FooterSettings, HomeCTA, PartnerBrand, SiteSettings


@admin.register(AboutPage)
class AboutPageAdmin(TranslationAdmin):
    fieldsets = (
        (
            _("Hero (page title / parallax)"),
            {
                "fields": (
                    "hero_background",
                    "hero_overlay",
                    "hero_title_main",
                    "hero_title_span",
                    "hero_breadcrumb_parent_label",
                ),
            },
        ),
        (
            _("Intro — image gallery (up to 4)"),
            {"fields": ("gallery_image_1", "gallery_image_2", "gallery_image_3", "gallery_image_4")},
        ),
        (
            _("Intro — text & button"),
            {
                "fields": (
                    "intro_title_main",
                    "intro_title_span",
                    "intro_lead",
                    "intro_body",
                    "intro_read_more_label",
                    "intro_read_more_url",
                ),
            },
        ),
        (_("Tabs — button labels"), {"fields": ("tab_mission_label", "tab_vision_label", "tab_values_label")}),
        (
            _("Tab: Mission"),
            {
                "fields": (
                    "mission_image",
                    "mission_heading_main",
                    "mission_heading_span",
                    "mission_lead",
                    "mission_body",
                ),
            },
        ),
        (
            _("Tab: Vision"),
            {
                "fields": (
                    "vision_image",
                    "vision_heading_main",
                    "vision_heading_span",
                    "vision_lead",
                    "vision_body",
                ),
            },
        ),
        (
            _("Tab: Values"),
            {
                "fields": (
                    "values_image",
                    "values_heading_main",
                    "values_heading_span",
                    "values_lead",
                    "values_body",
                ),
            },
        ),
        (
            _("Quality policy & “for you” (carousel section)"),
            {
                "description": _(
                    "Section title appears above the slider. "
                    "Slide 1: quality policy (title optional intro then one line per bullet). "
                    "Slide 2: “for you” block."
                ),
                "fields": (
                    "policy_section_background",
                    "policy_section_overlay",
                    "policy_section_title_main",
                    "policy_section_title_span",
                    "quality_policy_heading",
                    "quality_policy_teaser",
                    "quality_policy_points",
                    "for_you_heading",
                    "for_you_body",
                ),
            },
        ),
    )

    def has_add_permission(self, request):
        return not AboutPage.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ContactPage)
class ContactPageAdmin(TranslationAdmin):
    fieldsets = (
        (
            _("Hero (page title / parallax)"),
            {
                "fields": (
                    "hero_background",
                    "hero_overlay",
                    "hero_title_main",
                    "hero_title_span",
                    "hero_breadcrumb_parent_label",
                ),
            },
        ),
        (
            _("Left column (sidebar)"),
            {
                "fields": (
                    "sidebar_title_main",
                    "sidebar_title_span",
                    "sidebar_intro",
                ),
            },
        ),
        (
            _("Form area heading"),
            {
                "fields": ("form_heading_main", "form_heading_span"),
            },
        ),
    )

    def has_add_permission(self, request):
        return not ContactPage.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SiteSettings)
class SiteSettingsAdmin(TranslationAdmin):
    list_display = ('site_name', 'email', 'phone', 'default_language')
    fieldsets = (
        (
            _('Identity & contact'),
            {
                'fields': (
                    'site_name',
                    'logo',
                    'favicon',
                    'phone',
                    'email',
                    'whatsapp_number',
                    'address',
                    'map_embed_url',
                    'facebook',
                    'linkedin',
                    'instagram',
                    'default_language',
                ),
            },
        ),
        (
            _('Theme colors (HEX, e.g. #1d3338)'),
            {
                'description': _(
                    'Accent = buttons & links. Secondary accent = gradients. '
                    'Surface = page & light areas. Dark = header & footer.'
                ),
                'fields': (
                    'primary_color',
                    'secondary_color',
                    'surface_color',
                    'dark_color',
                ),
            },
        ),
    )


@admin.register(HomeCTA)
class HomeCTAAdmin(TranslationAdmin):
    list_display = ('__str__', 'is_active')
    fields = ('text_main', 'text_highlight', 'button_text', 'button_url', 'is_active')

    def has_add_permission(self, request):
        return not HomeCTA.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


class FooterLinkInline(TranslationTabularInline):
    model = FooterLink
    extra = 0
    fields = ('title', 'url', 'sort_order', 'is_active')


@admin.register(FooterSettings)
class FooterSettingsAdmin(TranslationAdmin):
    list_display = ('__str__',)
    inlines = (FooterLinkInline,)

    fieldsets = (
        (
            _("About column"),
            {
                'fields': ('about_heading_main', 'about_heading_span', 'about_text'),
            },
        ),
        (
            _("Solutions column (headings; links in table below)"),
            {
                'fields': ('solutions_heading_main', 'solutions_heading_span'),
            },
        ),
        (
            _("Recent posts column (title only — posts come from blog)"),
            {
                'fields': ('recent_heading_main', 'recent_heading_span'),
            },
        ),
        (
            _("Contact column"),
            {
                "description": _(
                    "Phone: link uses tel: (direct call). WhatsApp: digits only with country code — link opens chat in WhatsApp / web."
                ),
                "fields": ("address", "phone", "whatsapp_number", "email"),
            },
        ),
        (
            _("Footer bottom row"),
            {
                'fields': (
                    'footer_logo',
                    'hours_line1_label',
                    'hours_line1_value',
                    'hours_line2_label',
                    'hours_line2_value',
                ),
            },
        ),
        (
            _("Social media"),
            {
                'fields': (
                    'facebook_url',
                    'twitter_url',
                    'linkedin_url',
                    'instagram_url',
                    'youtube_url',
                ),
            },
        ),
        (
            _("Copyright line"),
            {
                'fields': ('copyright_suffix',),
            },
        ),
    )

    def has_add_permission(self, request):
        return not FooterSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(PartnerBrand)
class PartnerBrandAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "sort_order", "website_url")
    list_filter = ("is_active",)
    search_fields = ("name", "website_url")
    ordering = ("sort_order", "id")

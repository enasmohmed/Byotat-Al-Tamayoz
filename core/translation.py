from modeltranslation.translator import translator, TranslationOptions

from .models import AboutPage, ContactPage, FooterSettings, FooterLink, HomeCTA, SiteSettings


class SiteSettingsTranslationOptions(TranslationOptions):
    fields = ('site_name', 'address', 'phone', 'email')

translator.register(SiteSettings, SiteSettingsTranslationOptions)


class FooterSettingsTranslationOptions(TranslationOptions):
    fields = (
        'about_heading_main',
        'about_heading_span',
        'about_text',
        'solutions_heading_main',
        'solutions_heading_span',
        'recent_heading_main',
        'recent_heading_span',
        'contact_heading_main',
        'contact_heading_span',
        'address',
        'phone',
        'email',
        'hours_line1_label',
        'hours_line1_value',
        'hours_line2_label',
        'hours_line2_value',
        'copyright_suffix',
    )

translator.register(FooterSettings, FooterSettingsTranslationOptions)


class FooterLinkTranslationOptions(TranslationOptions):
    fields = ('title',)

translator.register(FooterLink, FooterLinkTranslationOptions)


class HomeCTATranslationOptions(TranslationOptions):
    fields = ('text_main', 'text_highlight', 'button_text')


translator.register(HomeCTA, HomeCTATranslationOptions)


class AboutPageTranslationOptions(TranslationOptions):
    fields = (
        "hero_title_main",
        "hero_title_span",
        "hero_breadcrumb_parent_label",
        "intro_title_main",
        "intro_title_span",
        "intro_lead",
        "intro_body",
        "intro_read_more_label",
        "tab_mission_label",
        "tab_vision_label",
        "tab_values_label",
        "mission_heading_main",
        "mission_heading_span",
        "mission_lead",
        "mission_body",
        "vision_heading_main",
        "vision_heading_span",
        "vision_lead",
        "vision_body",
        "values_heading_main",
        "values_heading_span",
        "values_lead",
        "values_body",
        "policy_section_title_main",
        "policy_section_title_span",
        "quality_policy_heading",
        "quality_policy_teaser",
        "quality_policy_points",
        "for_you_heading",
        "for_you_body",
    )


translator.register(AboutPage, AboutPageTranslationOptions)


class ContactPageTranslationOptions(TranslationOptions):
    fields = (
        "hero_title_main",
        "hero_title_span",
        "hero_breadcrumb_parent_label",
        "sidebar_title_main",
        "sidebar_title_span",
        "sidebar_intro",
        "form_heading_main",
        "form_heading_span",
    )


translator.register(ContactPage, ContactPageTranslationOptions)


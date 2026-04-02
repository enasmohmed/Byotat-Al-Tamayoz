from modeltranslation.translator import TranslationOptions, translator

from .models import Service, ServicesFeature, ServicesLanding


class ServiceTranslationOptions(TranslationOptions):
    fields = ("title", "short_description", "description")


translator.register(Service, ServiceTranslationOptions)


class ServicesLandingTranslationOptions(TranslationOptions):
    fields = (
        "hero_title_main",
        "hero_title_span",
        "breadcrumb_parent_label",
        "breadcrumb_current_label",
        "sidebar_title_main",
        "sidebar_title_span",
        "sidebar_intro",
    )


translator.register(ServicesLanding, ServicesLandingTranslationOptions)


class ServicesFeatureTranslationOptions(TranslationOptions):
    fields = ("title", "description")


translator.register(ServicesFeature, ServicesFeatureTranslationOptions)

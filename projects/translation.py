from modeltranslation.translator import translator, TranslationOptions
from .models import AllProjectsPageSettings, Project, ProjectCategory, SectionTitle





class ProjectTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "description",
        "city",
        "district",
        "rooms_options",
        "bathrooms_options",
        "card_badge_text",
        "card_badge_secondary_text",
    )

translator.register(Project, ProjectTranslationOptions)


class ProjectCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(ProjectCategory, ProjectCategoryTranslationOptions)


class SectionTitleTranslationOptions(TranslationOptions):
    fields = ('title', 'highlight', 'subtitle')

translator.register(SectionTitle, SectionTitleTranslationOptions)


class AllProjectsPageSettingsTranslationOptions(TranslationOptions):
    fields = ("hero_title_main", "hero_title_span", "breadcrumb_parent_label", "breadcrumb_current_label")


translator.register(AllProjectsPageSettings, AllProjectsPageSettingsTranslationOptions)
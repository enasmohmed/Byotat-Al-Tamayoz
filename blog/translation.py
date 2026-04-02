from modeltranslation.translator import TranslationOptions, translator

from .models import BlogListPageSettings, Post, PostCategory


class PostCategoryTranslationOptions(TranslationOptions):
    fields = ("name",)


translator.register(PostCategory, PostCategoryTranslationOptions)


class PostTranslationOptions(TranslationOptions):
    fields = ("title", "content")

translator.register(Post, PostTranslationOptions)


class BlogListPageSettingsTranslationOptions(TranslationOptions):
    fields = (
        "hero_title_main",
        "hero_title_span",
        "hero_intro",
        "breadcrumb_parent_label",
        "breadcrumb_current_label",
    )


translator.register(BlogListPageSettings, BlogListPageSettingsTranslationOptions)

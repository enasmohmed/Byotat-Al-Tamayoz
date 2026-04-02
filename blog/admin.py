from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin

import blog.translation  # noqa: F401

from .models import BlogListPageSettings, Post, PostCategory


@admin.register(PostCategory)
class PostCategoryAdmin(TranslationAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "name_ar", "name_en", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "slug", "language", "is_published", "display_date", "created_at")
    search_fields = ("title", "content")
    list_filter = ("is_published", "language", "category", "created_at")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "created_at"
    autocomplete_fields = ("category",)


@admin.register(BlogListPageSettings)
class BlogListPageSettingsAdmin(TranslationAdmin):
    fieldsets = (
        (
            _("Hero (page title / parallax)"),
            {
                "fields": (
                    "hero_background",
                    "hero_overlay",
                    "hero_title_main",
                    "hero_title_span",
                    "hero_intro",
                ),
            },
        ),
        (
            _("Breadcrumb"),
            {
                "fields": ("breadcrumb_parent_label", "breadcrumb_current_label"),
                "description": _("Leave labels empty to use the default translated strings."),
            },
        ),
    )

    def has_add_permission(self, request):
        return not BlogListPageSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

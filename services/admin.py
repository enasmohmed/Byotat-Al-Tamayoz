from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline

import services.translation  # noqa: F401 — register before TranslationAdmin

from .models import Service, ServicesFeature, ServicesLanding


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_active", "language")
    search_fields = ("title", "short_description", "description")
    list_filter = ("is_active", "language")


class ServicesFeatureInline(TranslationTabularInline):
    model = ServicesFeature
    extra = 0
    ordering = ("sort_order", "id")
    fields = ("title", "description", "icon_class", "sort_order", "is_promoted", "is_active")


@admin.register(ServicesLanding)
class ServicesLandingAdmin(TranslationAdmin):
    inlines = (ServicesFeatureInline,)
    fieldsets = (
        (
            _("Hero (page title / parallax)"),
            {
                "fields": (
                    "hero_background",
                    "hero_overlay",
                    "hero_title_main",
                    "hero_title_span",
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
        (
            _("Features block (grey section — sidebar title + intro)"),
            {
                "fields": (
                    "sidebar_title_main",
                    "sidebar_title_span",
                    "sidebar_intro",
                    "section_pattern_image",
                ),
            },
        ),
    )

    def has_add_permission(self, request):
        return not ServicesLanding.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

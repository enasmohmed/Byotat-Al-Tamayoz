from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin

import projects.translation  # noqa: F401

from .models import AllProjectsPageSettings, Project, ProjectCategory, ProjectGalleryImage, SectionTitle


class ProjectGalleryImageInline(admin.TabularInline):
    model = ProjectGalleryImage
    extra = 1
    ordering = ("sort_order", "id")


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(TranslationAdmin):
    list_display = ("name_ar", "slug", "default_language")
    list_filter = ("default_language",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Project)
class ProjectAdmin(TranslationAdmin):
    list_display = ("title_ar", "slug", "city", "area_key", "category", "is_active", "sold_percentage")
    search_fields = ("title", "description", "city", "district", "area_key")
    list_filter = ("category", "is_active", "default_language")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProjectGalleryImageInline]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "slug",
                    "description",
                    "image",
                    "promo_video",
                    "category",
                    "is_active",
                    "default_language",
                ),
            },
        ),
        (
            _("Location (display)"),
            {
                "fields": ("city", "district", "area_key"),
                "description": _("Use the same «Area grouping key» for projects in one zone to link «suggested»."),
            },
        ),
        (
            _("Specifications (real estate)"),
            {
                "fields": (
                    "area_sqm_min",
                    "area_sqm_max",
                    "area_sqm",
                    "room_count",
                    "rooms_options",
                    "bathroom_count",
                    "bathrooms_options",
                    "has_living_hall",
                    "has_elevator",
                    "has_private_parking",
                    "has_smart_home",
                    "has_maid_room",
                    "has_driver_room",
                ),
            },
        ),
        (
            _("Sales"),
            {"fields": ("sold_percentage",)},
        ),
        (
            _("Guarantees"),
            {
                "fields": (
                    "structural_warranty_years",
                    "warranty_plumbing",
                    "warranty_water_heaters",
                    "warranty_smart_control",
                    "warranty_electrical_switches",
                    "warranty_electrical_extensions",
                    "warranty_faucets",
                    "warranty_lighting",
                ),
            },
        ),
        (_("Map"), {"fields": ("map_embed_url",)}),
    )


@admin.register(AllProjectsPageSettings)
class AllProjectsPageSettingsAdmin(TranslationAdmin):
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
    )

    def has_add_permission(self, request):
        return not AllProjectsPageSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SectionTitle)
class SectionTitleAdmin(TranslationAdmin):
    list_display = ("title_ar", "highlight_ar", "subtitle_ar")
    search_fields = ("title_ar", "title_en", "highlight_ar", "highlight_en", "subtitle_ar", "subtitle_en")

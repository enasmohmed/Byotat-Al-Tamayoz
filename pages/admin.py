import pages.translation  # noqa: F401 — modeltranslation

from django.contrib import admin

from core.unfold_bases import UnfoldTranslationAdmin

from .models import Page


# ---- Admin للـ Page ----
@admin.register(Page)
class PageAdmin(UnfoldTranslationAdmin):
    list_display = ('title', 'slug', 'is_active', 'language')
    search_fields = ('title', 'content')
    list_filter = ('is_active', 'language')


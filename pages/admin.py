from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Page


# ---- Admin للـ Page ----
@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_active', 'language')
    search_fields = ('title', 'content')
    list_filter = ('is_active', 'language')


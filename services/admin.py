from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Service



@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_active', 'language')
    search_fields = ('title', 'short_description', 'description')
    list_filter = ('is_active', 'language')

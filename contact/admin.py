import contact.translation  # noqa: F401 — modeltranslation

from django.contrib import admin

from .models import ContactMessage




@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "subject", "send_via", "is_read", "created_at")
    search_fields = ("name", "email", "phone", "subject", "message")
    list_filter = ("is_read", "send_via", "created_at")

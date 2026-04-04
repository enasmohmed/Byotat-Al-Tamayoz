"""عناصر عرض مشتركة في لوحة التحكم (مصغّرات صور، إلخ)."""

from __future__ import annotations

from django.utils.html import format_html
from django.utils.safestring import mark_safe


def admin_image_thumbnail(
    image_field,
    *,
    size_px: int = 56,
    alt: str = "",
) -> str:
    """يُرجع وسم img آمناً لقائمة التغيير، أو شرطة إن لم تتوفر صورة."""
    if not image_field:
        return mark_safe('<span class="admin-thumb-empty">—</span>')
    try:
        url = image_field.url
    except (ValueError, AttributeError):
        return mark_safe('<span class="admin-thumb-empty">—</span>')
    return format_html(
        '<img class="admin-list-thumb" src="{}" alt="{}" width="{}" height="{}" loading="lazy" />',
        url,
        alt,
        size_px,
        size_px,
    )

"""
شعار وفافيكون لوحة Unfold من إعدادات الموقع (Site settings) مع بدائل ثابتة.
"""

from django.templatetags.static import static


def _site():
    from core.models import SiteSettings

    return SiteSettings.objects.first()


def unfold_admin_logo_url(request):
    site = _site()
    if site and getattr(site, "logo", None):
        return site.logo.url
    return static("ltr/images/logo-yellow.png")


def unfold_admin_favicon_url(request):
    site = _site()
    if site and getattr(site, "favicon", None):
        return site.favicon.url
    return static("ltr/images/favicon.ico")

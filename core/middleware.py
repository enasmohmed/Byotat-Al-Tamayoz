"""
Middleware for locale: keep Django admin aligned with site language when possible.
"""

from django.conf import settings
from django.utils import translation
from django.utils.translation import check_for_language


class AdminSiteLanguageMiddleware:
    """
    On /admin/, use the language cookie (same as django.views.i18n.set_language).
    Django 6+ no longer uses LANGUAGE_SESSION_KEY — language is stored in a cookie.

    If there is no valid cookie, use LANGUAGE_CODE so the admin matches the site
    default instead of only the browser Accept-Language header.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/admin/"):
            allowed = {code for code, _ in settings.LANGUAGES}
            lang = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
            if not lang or lang not in allowed or not check_for_language(lang):
                lang = settings.LANGUAGE_CODE
            translation.activate(lang)
            request.LANGUAGE_CODE = lang
        return self.get_response(request)

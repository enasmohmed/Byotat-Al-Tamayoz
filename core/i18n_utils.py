from django.conf import settings
from django.utils import translation


def interface_language(request):
    """لغة الواجهة = نفس قرار LocaleMiddleware ومتغير LANGUAGE_CODE في القالب.

    لا نفضّل الكوكي على get_language() هنا؛ ده كان يسبب عكس التايتل عن اتجاه الصفحة.
    الكوكي يُستخدم فقط لو LANGUAGE_CODE و get_language() مش متاحين.
    """
    raw = (
        getattr(request, 'LANGUAGE_CODE', None)
        or translation.get_language()
        or request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
        or 'ar'
    )
    lang = (raw or 'ar').split('-')[0].lower()
    if lang not in ('ar', 'en'):
        lang = 'ar'
    return lang

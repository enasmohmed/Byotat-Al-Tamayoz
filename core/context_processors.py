from django.conf import settings
from django.utils import translation

from blog.models import Post
from core.i18n_utils import interface_language
from core.models import FooterSettings, SiteSettings


def _site_name_for_language(site, lang):
    """
    اسم الموقع حسب لغة الواجهة؛ لو حقل اللغة الحالية فاضي نكمّل بترتيب يعتمد default_language في الإعدادات.
    """
    if not site:
        return ''
    lang = (lang or 'ar').split('-')[0].lower()
    if lang not in ('ar', 'en'):
        lang = 'ar'
    en = (getattr(site, 'site_name_en', None) or '').strip()
    ar = (getattr(site, 'site_name_ar', None) or '').strip()
    base = (getattr(site, 'site_name', None) or '').strip()
    dl = getattr(site, 'default_language', None) or 'ar'
    if dl not in ('ar', 'en'):
        dl = 'ar'

    if lang == 'en':
        if en:
            return en
        if dl == 'en':
            return base or ar
        return ar or base

    if ar:
        return ar
    if dl == 'ar':
        return base or en
    return en or base


def _hex_color(site, attr, fallback):
    if not site:
        return fallback
    v = getattr(site, attr, None)
    if v and str(v).strip():
        return str(v).strip()
    return fallback


# def site_settings(request):
#     site = SiteSettings.objects.first()  # أو اختاري حسب id
#     return {'site': site}


def site_settings(request):
    """
    Inject site-wide settings into all templates.
    يعتمد على أول سجل من SiteSettings كإعدادات عامة للموقع.
    """
    # نفس لغة القالب (LANGUAGE_CODE): LocaleMiddleware ثم get_language (انظر interface_language)
    lang = interface_language(request)
    translation.activate(lang)

    site = SiteSettings.objects.first()
    footer = FooterSettings.objects.first()
    footer_recent = list(
        Post.objects.filter(is_published=True, language=lang).order_by('-created_at')[:2]
    )
    if not footer_recent:
        footer_recent = list(Post.objects.filter(is_published=True).order_by('-created_at')[:2])
    footer_links = []
    if footer:
        footer_links = list(footer.links.filter(is_active=True).order_by('sort_order', 'id'))

    site_display_name = _site_name_for_language(site, lang)
    if not (site_display_name or "").strip():
        site_display_name = (getattr(settings, "SITE_TITLE_FALLBACK", None) or "").strip() or "Site"

    data = {
        'site_name': site_display_name,
        'primary_color': _hex_color(site, 'primary_color', '#cc9955'),
        'secondary_color': _hex_color(site, 'secondary_color', '#cc9955'),
        'surface_color': _hex_color(site, 'surface_color', '#ececec'),
        'dark_color': _hex_color(site, 'dark_color', '#1d3338'),
        'phone': site.phone if site else '',
        'email': site.email if site else '',
        'address': site.address if site else '',
        'facebook': site.facebook if site else '',
        'linkedin': site.linkedin if site else '',
        'instagram': site.instagram if site else '',
        # لو مفيش إعدادات بنفترض العربي كافتراضي للموقع
        'default_language': site.default_language if site else 'ar',
        'logo_url': (
            site.logo.url
            if site and site.logo
            else '/static/ltr/images/logo-yellow.png'
        ),
        'favicon_url': (
            site.favicon.url
            if site and site.favicon
            else '/static/ltr/images/favicon.ico'
        ),
    }

    footer_logo_url = (
        footer.footer_logo.url
        if footer and footer.footer_logo
        else data['logo_url']
    )

    return {
        # الـ object نفسه لو حابة تستخدميه
        'site': site,
        'footer': footer,
        'footer_links': footer_links,
        'footer_recent_posts': footer_recent,
        'footer_logo_url': footer_logo_url,
        "map_embed_default": getattr(settings, "DEFAULT_MAP_EMBED_URL", "") or "",

        # نسخة منظمة جاهزة للاستخدام
        'site_settings': data,

        # اختصارات مباشرة
        'primary_color': data['primary_color'],
        'secondary_color': data['secondary_color'],
        'surface_color': data['surface_color'],
        'dark_color': data['dark_color'],
        'default_language': data['default_language'],
        'logo_url': data['logo_url'],
        'favicon_url': data['favicon_url'],
    }

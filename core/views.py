import hashlib

from django.utils.text import slugify
from django.views.generic import TemplateView
from blog.models import Post
from core.i18n_utils import interface_language
from core.models import AboutPage, HomeCTA, PartnerBrand, SiteSettings
from projects.models import SectionTitle, Project


def _section_display(section, lang):
    """نصوص القسم للغة المطلوبة مع احتياط: العربي ثم الإنجليزي."""
    if not section:
        return None
    if lang not in ('ar', 'en'):
        lang = 'ar'
    title = (getattr(section, 'title_%s' % lang, None) or
             getattr(section, 'title_ar', None) or
             getattr(section, 'title_en', None) or '')
    highlight = (getattr(section, 'highlight_%s' % lang, None) or
                 getattr(section, 'highlight_ar', None) or
                 getattr(section, 'highlight_en', None) or '')
    subtitle = (getattr(section, 'subtitle_%s' % lang, None) or
                getattr(section, 'subtitle_ar', None) or
                getattr(section, 'subtitle_en', None) or '')
    return {'title': title, 'highlight': highlight, 'subtitle': subtitle}


def _location_filter_class(prefix: str, raw: str) -> str:
    raw = (raw or "").strip()
    if not raw:
        return ""
    s = slugify(raw)
    if s:
        return f"{prefix}-{s}"
    digest = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]
    return f"{prefix}-u{digest}"


class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site'] = SiteSettings.objects.first()
        lang = interface_language(self.request)

        sections = list(SectionTitle.objects.all().order_by("id"))
        section_projects = sections[0] if len(sections) > 0 else None
        section_partners = sections[1] if len(sections) > 1 else None
        section_news = sections[2] if len(sections) > 2 else None

        context['section_projects'] = section_projects
        context['section_projects_display'] = _section_display(section_projects, lang)
        context['section_partners'] = section_partners
        context['section_partners_display'] = _section_display(section_partners, lang)
        context['section_news_display'] = _section_display(section_news, lang)

        plist = list(Project.objects.filter(is_active=True).select_related("category"))
        city_labels = {}
        for p in plist:
            city = (getattr(p, "city", None) or "").strip()
            p.filter_city_class = _location_filter_class("ct", city) if city else ""
            if p.filter_city_class:
                city_labels[p.filter_city_class] = city
        context["projects"] = plist
        context["filter_cities"] = sorted(city_labels.items(), key=lambda x: x[1].casefold())
        context["partner_brands"] = PartnerBrand.objects.filter(is_active=True).order_by("sort_order", "id")
        context["home_cta"] = HomeCTA.objects.filter(is_active=True).first()

        # مقالات بنفس لغة الواجهة؛ لو مفيش (مثلاً بوستات قديمة بلغة تانية)، نعرض آخر المنشور
        latest = list(
            Post.objects.filter(is_published=True, language=lang).order_by("-created_at")[:3]
        )
        if not latest:
            latest = list(Post.objects.filter(is_published=True).order_by("-created_at")[:3])
        context["latest_posts"] = latest
        return context


class AboutUsView(TemplateView):
    template_name = "about_us.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        about_page = AboutPage.objects.first()
        context["about_page"] = about_page
        gallery_urls = []
        if about_page:
            for i in range(1, 5):
                img = getattr(about_page, f"gallery_image_{i}", None)
                if img:
                    gallery_urls.append(img.url)
        context["about_gallery_urls"] = gallery_urls
        quality_lines = []
        if about_page and about_page.quality_policy_points:
            quality_lines = [
                ln.strip()
                for ln in about_page.quality_policy_points.splitlines()
                if ln.strip()
            ]
        context["quality_policy_lines"] = quality_lines
        has_quality_block = bool(
            about_page
            and (
                (about_page.quality_policy_heading or "").strip()
                or (about_page.quality_policy_teaser or "").strip()
                or quality_lines
            )
        )
        has_for_you_block = bool(
            about_page
            and (
                (about_page.for_you_heading or "").strip()
                or (about_page.for_you_body or "").strip()
            )
        )
        context["show_about_policy_section"] = bool(
            about_page and (has_quality_block or has_for_you_block)
        )
        return context

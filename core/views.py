from collections import defaultdict
from django.views.generic import TemplateView
from blog.models import Post
from core.i18n_utils import interface_language
from core.models import AboutPage, HomeCTA, PartnerBrand, SiteSettings
from projects.models import SectionTitle, Project

HOME_PROJECTS_MAX = 6

# Masonry tile height variants (cycle) — kept for annotate compatibility (home uses carousel now)
HOME_MSNRY_VARIANTS = (
    "hp-msnry--sq",
    "hp-msnry--short",
    "hp-msnry--short",
    "hp-msnry--sq",
    "hp-msnry--short",
    "hp-msnry--sq",
)


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


def _project_sort_key(p):
    return (
        0 if (p.image and getattr(p.image, "name", "")) else 1,
        -(p.pk or 0),
    )


def _pick_home_projects_mixed(all_projects: list, limit: int) -> list:
    """
    Pick up to `limit` projects, round-robin across statuses so «All» shows a status mix.
    Projects without an explicit status token fill in at the end.
    """
    buckets: dict[str, list] = defaultdict(list)
    for p in all_projects:
        status = getattr(p, "status_filter_class", "") or ""
        token = status.strip()
        buckets[token].append(p)
    for token in buckets:
        buckets[token].sort(key=_project_sort_key)

    nonempty = [t for t in buckets if t and buckets[t]]
    status_order = {f"st-{value}": idx for idx, (value, _label) in enumerate(Project.ProjectStatus.choices)}
    nonempty.sort(key=lambda t: status_order.get(t, 999))
    ordered_tokens = nonempty + ([""] if buckets.get("") else [])

    picked = []
    while len(picked) < limit and any(buckets[t] for t in buckets):
        moved = False
        for t in ordered_tokens:
            if len(picked) >= limit:
                break
            if buckets[t]:
                picked.append(buckets[t].pop(0))
                moved = True
        if not moved:
            break

    if len(picked) < limit:
        seen = {id(x) for x in picked}
        rest = [p for p in all_projects if id(p) not in seen]
        rest.sort(key=_project_sort_key)
        for p in rest:
            if len(picked) >= limit:
                break
            picked.append(p)
    return picked


def annotate_home_projects_for_home(qs_home: list):
    """
    Mutate each project in qs_home with filter_status_class, home_msnry_variant, home_in_mix.
    Home view passes at most HOME_PROJECTS_MAX projects; the template may set home_in_mix on all for «All».
    Status filter matches .st-* classes on carousel slides.
    """
    status_order = []
    for value, _label in Project.ProjectStatus.choices:
        token = f"st-{value}"
        status_order.append((token, Project.status_label_for_value(value)))
    mix_pks = {p.pk for p in _pick_home_projects_mixed(qs_home, HOME_PROJECTS_MAX)}
    n_var = len(HOME_MSNRY_VARIANTS)
    for i, p in enumerate(qs_home):
        p.filter_status_class = p.status_filter_class
        p.home_msnry_variant = HOME_MSNRY_VARIANTS[i % n_var]
        p.home_in_mix = p.pk in mix_pks
    return status_order


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

        qs_home_all = list(
            Project.objects.filter(is_active=True)
            .select_related("category")
            .order_by("-id")
        )
        qs_home = _pick_home_projects_mixed(qs_home_all, HOME_PROJECTS_MAX)
        context["filter_statuses"] = annotate_home_projects_for_home(qs_home)
        for p in qs_home:
            p.home_in_mix = True
        context["projects"] = qs_home
        context["partner_brands"] = PartnerBrand.objects.filter(is_active=True).order_by("sort_order", "id")
        context["home_cta"] = HomeCTA.objects.filter(is_active=True).first()

        # كل مقالات الأخبار المنشورة بنفس لغة الواجهة (سلايدر الصفحة الرئيسية)
        latest = list(
            Post.objects.filter(is_published=True, language=lang)
            .select_related("category")
            .order_by("-created_at")
        )
        if not latest:
            latest = list(
                Post.objects.filter(is_published=True)
                .select_related("category")
                .order_by("-created_at")
            )
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

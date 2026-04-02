import hashlib
from collections import defaultdict

from django.utils.text import slugify
from django.views.generic import ListView, DetailView

from core.i18n_utils import interface_language

from .models import AllProjectsPageSettings, Project


def _location_filter_class(prefix: str, raw: str) -> str:
    raw = (raw or "").strip()
    if not raw:
        return ""
    slug = slugify(raw)
    if slug:
        return f"{prefix}-{slug}"
    digest = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]
    return f"{prefix}-u{digest}"


class ProjectListView(ListView):
    model = Project
    template_name = "all_projects.html"
    context_object_name = "projects"

    def get_queryset(self):
        return Project.objects.filter(is_active=True).select_related("category")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lang = interface_language(self.request)
        context["all_projects_page"] = AllProjectsPageSettings.objects.first()
        context["interface_lang"] = lang

        plist = list(context["projects"])
        city_labels = {}
        dist_labels = {}
        by_city = defaultdict(dict)

        for p in plist:
            city = (getattr(p, "city", None) or "").strip()
            district = (getattr(p, "district", None) or "").strip()
            p.filter_city_class = _location_filter_class("ct", city) if city else ""
            p.filter_district_class = _location_filter_class("dt", district) if district else ""
            if p.filter_city_class:
                city_labels[p.filter_city_class] = city
            if p.filter_district_class:
                dist_labels[p.filter_district_class] = district
            if p.filter_city_class and p.filter_district_class:
                by_city[p.filter_city_class][p.filter_district_class] = district

        context["projects"] = plist
        context["filter_cities"] = sorted(city_labels.items(), key=lambda x: x[1].casefold())
        districts_by_city = {
            ct: [{"v": dt, "l": lab} for dt, lab in sorted(dmap.items(), key=lambda x: x[1].casefold())]
            for ct, dmap in by_city.items()
        }
        context["districts_by_city"] = districts_by_city
        context["all_districts_options"] = [
            {"v": dt, "l": lab} for dt, lab in sorted(dist_labels.items(), key=lambda x: x[1].casefold())
        ]
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = "blog-details.html"
    context_object_name = "project"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Project.objects.filter(is_active=True).select_related("category").prefetch_related("gallery_images")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object

        main_url = project.image.url if project.image else None
        gallery_urls = []
        if main_url:
            gallery_urls.append(main_url)
        for gi in project.gallery_images.all():
            u = gi.image.url
            if u not in gallery_urls:
                gallery_urls.append(u)
        if not gallery_urls:
            for gi in project.gallery_images.all():
                gallery_urls.append(gi.image.url)
        context["project_gallery_urls"] = gallery_urls

        qs = (
            Project.objects.filter(is_active=True)
            .select_related("category")
            .prefetch_related("gallery_images")
            .exclude(pk=project.pk)
        )

        suggested = []
        seen = set()

        def add_from(iterable, limit=8):
            for p in iterable:
                if p.pk in seen:
                    continue
                seen.add(p.pk)
                suggested.append(p)
                if len(suggested) >= limit:
                    break

        # Suggested projects: keep recommendations within the same city.
        # (Avoid showing Makkah projects while viewing a Jeddah project, etc.)
        city = (project.city or "").strip()
        district = (project.district or "").strip()

        if city:
            qs_city = qs.filter(city=city)
            if district:
                add_from(qs_city.filter(district=district))
            add_from(qs_city)
        else:
            # If city isn't set, fall back to the previous strategy (best-effort).
            if (project.area_key or "").strip():
                add_from(qs.filter(area_key=project.area_key))
            if len(suggested) < 4 and district:
                add_from(qs.filter(district=district))
            if len(suggested) < 4 and project.category_id:
                add_from(qs.filter(category_id=project.category_id))
            if len(suggested) < 4:
                add_from(qs.order_by("id"))

        context["suggested_projects"] = suggested[:4]

        context["has_specs_tab"] = any(
            [
                project.area_sqm is not None,
                project.area_sqm_min is not None,
                project.area_sqm_max is not None,
                project.room_count is not None,
                (getattr(project, "rooms_options", "") or "").strip(),
                project.bathroom_count is not None,
                (getattr(project, "bathrooms_options", "") or "").strip(),
                project.has_living_hall,
                project.has_elevator,
                project.has_private_parking,
                project.has_smart_home,
                project.has_maid_room,
                getattr(project, "has_driver_room", False),
            ]
        )
        context["has_guarantees_tab"] = any(
            [
                project.structural_warranty_years,
                (project.warranty_plumbing or "").strip(),
                (project.warranty_water_heaters or "").strip(),
                (getattr(project, "warranty_smart_control", "") or "").strip(),
                (project.warranty_electrical_switches or "").strip(),
                (project.warranty_electrical_extensions or "").strip(),
                (project.warranty_faucets or "").strip(),
                (project.warranty_lighting or "").strip(),
            ]
        )
        raw_map = (project.map_embed_url or "").strip()
        if raw_map and "<iframe" in raw_map.lower():
            context["map_embed_block"] = raw_map
            context["map_embed_src"] = None
        else:
            context["map_embed_block"] = None
            context["map_embed_src"] = raw_map or None
        context["has_location_tab"] = bool(raw_map)
        context["has_video_tab"] = bool(getattr(project.promo_video, "name", None))
        context["show_project_tabs"] = (
            context["has_specs_tab"]
            or context["has_guarantees_tab"]
            or context["has_location_tab"]
            or context["has_video_tab"]
        )
        if context["has_specs_tab"]:
            context["first_project_tab"] = "specs"
        elif context["has_guarantees_tab"]:
            context["first_project_tab"] = "guarantees"
        elif context["has_location_tab"]:
            context["first_project_tab"] = "location"
        elif context["has_video_tab"]:
            context["first_project_tab"] = "video"
        else:
            context["first_project_tab"] = None
        return context

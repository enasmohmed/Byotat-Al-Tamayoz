from django.views.generic import ListView, DetailView

from core.i18n_utils import interface_language

from .models import AllProjectsPageSettings, Project


class ProjectListView(ListView):
    model = Project
    template_name = "all_projects.html"
    context_object_name = "projects"
    paginate_by = 6

    def get_queryset(self):
        selected_status = (self.request.GET.get("status") or "").strip()
        selected_district = (self.request.GET.get("district") or "").strip()
        status_values = {value for value, _label in Project.ProjectStatus.choices}

        projects = list(
            Project.objects.filter(is_active=True)
            .select_related("category")
            .order_by("-id")
        )
        if selected_status in status_values:
            projects = [p for p in projects if p.effective_status_for_filters == selected_status]
        if selected_district:
            projects = [p for p in projects if (getattr(p, "district", "") or "").strip() == selected_district]
        return projects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lang = interface_language(self.request)
        context["all_projects_page"] = AllProjectsPageSettings.objects.first()
        context["interface_lang"] = lang
        context["selected_status"] = (self.request.GET.get("status") or "").strip()
        context["selected_district"] = (self.request.GET.get("district") or "").strip()

        status_order = [(value, Project.status_label_for_value(value)) for value, _label in Project.ProjectStatus.choices]
        context["filter_statuses"] = status_order

        all_projects = Project.objects.filter(is_active=True).only("district")
        districts = sorted(
            {(p.district or "").strip() for p in all_projects if (p.district or "").strip()},
            key=str.casefold,
        )
        context["all_districts_options"] = districts

        query = self.request.GET.copy()
        query.pop("page", None)
        context["filters_query"] = query.urlencode()
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = "projects/project_detail.html"
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

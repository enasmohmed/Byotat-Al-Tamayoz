from django.views.generic import DetailView, TemplateView

from .models import Service, ServicesLanding


class ServicesLandingView(TemplateView):
    template_name = "services.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        landing = ServicesLanding.objects.first()
        ctx["services_landing"] = landing
        promoted = None
        grid = []
        if landing:
            feats = list(landing.features.filter(is_active=True).order_by("sort_order", "id"))
            promoted = next((f for f in feats if f.is_promoted), None)
            if promoted is None and feats:
                promoted = feats[0]
                grid = feats[1:]
            elif promoted:
                grid = [f for f in feats if f.pk != promoted.pk]
        ctx["services_feature_promoted"] = promoted
        ctx["services_features_grid"] = grid
        return ctx


class ServiceDetailView(DetailView):
    model = Service
    template_name = "services/service_detail.html"
    context_object_name = "service"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Service.objects.filter(is_active=True)

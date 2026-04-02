from django.urls import path, re_path

from .views import ServiceDetailView, ServicesLandingView

urlpatterns = [
    path("", ServicesLandingView.as_view(), name="services_list"),
    re_path(r"^(?P<slug>[^/]+)/$", ServiceDetailView.as_view(), name="service_detail"),
]

from django.urls import path
from .views import AboutUsView, HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about-us/', AboutUsView.as_view(), name='about_us'),
]

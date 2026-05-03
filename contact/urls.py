from django.urls import path
from .views import ContactFormView
from .whatsapp_receiver import whatsapp_contact_webhook

urlpatterns = [
    path('', ContactFormView.as_view(), name='contact_form'),
    path("api/whatsapp/", whatsapp_contact_webhook, name="contact_whatsapp_webhook"),
]

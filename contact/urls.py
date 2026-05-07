from django.urls import path
from .views import ContactFormView, contact_phone_exists
from .whatsapp_receiver import whatsapp_contact_webhook

urlpatterns = [
    path('', ContactFormView.as_view(), name='contact_form'),
    path("api/phone-exists/", contact_phone_exists, name="contact_phone_exists"),
    path("api/whatsapp/", whatsapp_contact_webhook, name="contact_whatsapp_webhook"),
]

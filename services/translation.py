from modeltranslation.translator import translator, TranslationOptions
from .models import Service

class ServiceTranslationOptions(TranslationOptions):
    fields = ('title', 'short_description', 'description')

translator.register(Service, ServiceTranslationOptions)

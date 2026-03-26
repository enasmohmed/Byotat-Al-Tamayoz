from modeltranslation.translator import translator, TranslationOptions
from .models import ContactMessage

class ContactMessageTranslationOptions(TranslationOptions):
    fields = ('name', 'subject', 'message')

translator.register(ContactMessage, ContactMessageTranslationOptions)

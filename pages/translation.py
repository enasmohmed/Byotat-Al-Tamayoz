from modeltranslation.translator import translator, TranslationOptions
from .models import Page

class PageTranslationOptions(TranslationOptions):
    fields = ('title', 'content')  # غير الحقول حسب الموديل بتاعك

translator.register(Page, PageTranslationOptions)

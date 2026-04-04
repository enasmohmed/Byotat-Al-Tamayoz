"""
قواعد أدمن موحّدة مع Django Unfold + modeltranslation.

- compressed_fields: تسمية الحقل بجانب الإدخال (مثل واجهة Unfold الافتراضية).
"""

from unfold.admin import ModelAdmin as UnfoldModelAdmin
from modeltranslation.admin import TranslationAdmin


class UnfoldTranslationAdmin(UnfoldModelAdmin, TranslationAdmin):
    compressed_fields = True


class UnfoldSiteModelAdmin(UnfoldModelAdmin):
    compressed_fields = True

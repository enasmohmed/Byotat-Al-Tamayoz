"""Date formatting that respects a given UI language (Arabic month names, etc.)."""

from datetime import date, datetime

from django import template
from django.utils import formats, translation
from django.utils.timezone import is_aware, localtime

register = template.Library()

# Gregorian month names — Django's bundled ``ar`` locale often leaves English ``F`` untranslated.
_AR_GREGORIAN_MONTHS = (
    "",
    "يناير",
    "فبراير",
    "مارس",
    "أبريل",
    "مايو",
    "يونيو",
    "يوليو",
    "أغسطس",
    "سبتمبر",
    "أكتوبر",
    "نوفمبر",
    "ديسمبر",
)

# Python weekday: Monday = 0 … Sunday = 6
_AR_WEEKDAYS = (
    "الاثنين",
    "الثلاثاء",
    "الأربعاء",
    "الخميس",
    "الجمعة",
    "السبت",
    "الأحد",
)
_EN_WEEKDAYS = (
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
)
_EN_GREGORIAN_MONTHS = (
    "",
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
)


def _to_naive_local_date(value):
    if isinstance(value, datetime):
        if is_aware(value):
            value = localtime(value)
        return value.date()
    if isinstance(value, date):
        return value
    return value


def _format_ar_day_month_year(d: date) -> str:
    return f"{d.day} {_AR_GREGORIAN_MONTHS[d.month]}، {d.year}"


def _format_ar_weekday_line(d: date) -> str:
    """e.g. الثلاثاء، 21 نوفمبر 2023"""
    wd = _AR_WEEKDAYS[d.weekday()]
    return f"{wd}، {d.day} {_AR_GREGORIAN_MONTHS[d.month]} {d.year}"


def _format_en_weekday_line(d: date) -> str:
    """e.g. Tuesday, 21 November 2023"""
    wd = _EN_WEEKDAYS[d.weekday()]
    return f"{wd}, {d.day} {_EN_GREGORIAN_MONTHS[d.month]} {d.year}"


@register.simple_tag
def locale_date(value, lang, fmt="DATE_FORMAT"):
    """
    Format *value* using Django locale formats under *lang* (e.g. 'ar', 'en').
    * LONG_DATE — weekday, day month year (Arabic or English).
    * DATE_FORMAT — for Arabic: day + Arabic month + year (no weekday).
    *fmt* otherwise: SHORT_DATE_FORMAT, DATETIME_FORMAT, …
    """
    if not value:
        return ""
    lang = (lang or "ar").split("-")[0].lower()
    if lang not in ("ar", "en"):
        lang = "ar"

    allowed = (
        "DATE_FORMAT",
        "SHORT_DATE_FORMAT",
        "DATETIME_FORMAT",
        "SHORT_DATETIME_FORMAT",
        "LONG_DATE",
    )
    if fmt not in allowed:
        fmt = "DATE_FORMAT"

    d = _to_naive_local_date(value)
    if fmt == "LONG_DATE":
        if not isinstance(d, date):
            return ""
        if lang == "ar":
            return _format_ar_weekday_line(d)
        return _format_en_weekday_line(d)

    if lang == "ar" and fmt == "DATE_FORMAT":
        if isinstance(d, date):
            return _format_ar_day_month_year(d)

    with translation.override(lang):
        return formats.date_format(value, fmt)

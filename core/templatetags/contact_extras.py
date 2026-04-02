import re

from django import template

register = template.Library()


@register.filter
def phone_digits(value):
    """Strip to digits for tel: links (keeps dialing reliable across + / spaces / dashes)."""
    if value is None:
        return ""
    return re.sub(r"\D+", "", str(value))

import re

from django import template


register = template.Library()

@register.filter
def index(sequence, position):
    return sequence[position]


@register.filter
def placeholder(value, token):
	value.field.widget.attrs["placeholder"] = token
	return value

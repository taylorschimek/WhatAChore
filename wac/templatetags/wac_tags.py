from django import template

register = template.Library()

@register.filter
def index(sequence, position):
    # print("tag {}".format(position))
    # print("tag done {}".format(sequence[position]))
    return sequence[position]

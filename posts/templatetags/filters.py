from django import template

register = template.Library()

@register.filter(name='multiply_by_20')
def multiply_by_20(value):
    return value * 20
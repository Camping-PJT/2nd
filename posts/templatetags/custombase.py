from django import template
from posts.models import Facility, Post

register = template.Library()

@register.simple_tag
def load_facilities():
    choices = Facility.FACILITY_CHOICES
    facilities = [choice[1] for choice in choices]
    return facilities


@register.simple_tag
def load_natures():
    n_choices = Post.NATURE_CHOICES
    natures = [choice[1] for choice in n_choices]
    return natures

@register.simple_tag
def load_categories():
    c_choices = Post.CATEGORY_CHOICES
    categories = [choice[1] for choice in c_choices]
    return categories

# app/templatetags/shuffle.py
import random
from django import template
register = template.Library()

@register.filter
def shuffle(arg):
    ary = list(arg)[:]
    random.shuffle(ary)
    return ary

from django import template
register = template.Library()

@register.filter
def repl_sc(value):
    return value.replace('\n','; ')

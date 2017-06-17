from django import template
register = template.Library()

@register.filter
def to_mp3(value):
    return 'mp3/Qus_{:02d}.mp3'.format(value)

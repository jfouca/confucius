from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.filter
def active(name, request):
    if request.path.startswith(reverse(name)):
        return 'active'
    return ''


@register.filter
def type(field):
    return field.field.__class__.__name__

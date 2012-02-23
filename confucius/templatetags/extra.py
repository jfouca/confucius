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
    if field.field.widget.__class__.__name__ is 'PasswordInput':
        return 'password'
    if field.field.__class__.__name__ is 'EmailField':
        return 'email'
    return 'text'

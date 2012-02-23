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
    if field.field.widget.__class__.__name__ is 'Select':
        return 'select'
    if field.field.widget.__class__.__name__ is 'SelectMultiple':
        return 'selectm'
    if field.field.widget.__class__.__name__ is 'CheckboxInput':
        return 'checkbox'
    if field.field.widget.__class__.__name__ is 'Textarea':
        return 'textarea'
    if field.field.widget.__class__.__name__ is 'PasswordInput':
        return 'password'
    if field.field.__class__.__name__ is 'EmailField':
        return 'email'
    return 'text'

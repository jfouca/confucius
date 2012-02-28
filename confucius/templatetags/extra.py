from django import template
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def no_time_left(date):
    """for icon in subtopbar"""
    pass


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
    if field.field.__class__.__name__ is 'DateField':
        return 'date'
    if field.field.__class__.__name__ is 'EmailField':
        return 'email'
    return 'text'

@register.filter
def small(field):
    return field.as_widget(attrs={'class': 'input-small'})

@register.filter
def medium(field):
    return field.as_widget(attrs={'class': 'input-medium'})

@register.filter
def large(field):
    return field.as_widget(attrs={'class': 'input-large'})

@register.filter
def textarea(field):
    return field.as_widget(attrs={'class': 'input-large', 'rows': '3'})

@register.filter
def bigtextarea(field):
    return field.as_widget(attrs={'class': 'input-xxlarge', 'rows': '6'})

@register.filter
def calendar(field):
    return field.as_widget(attrs={'class': 'input-small datepicker'})

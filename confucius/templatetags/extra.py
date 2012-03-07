from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def active(name, request):
    if name in request.path:
        return 'active'
    return ''


@register.filter
def icon_active(name, request):
    if name in request.path:
        return 'icon-white'
    return ''
    

@register.filter
def icon(field):
    try:
        if type(field) == 'password':
            return 'lock'
        if type(field) in ('text', 'date', 'select', 'selectm'):
            return 'pencil'
        if type(field) == 'email':
            return 'envelope'
    except:
        pass


@register.filter
def type(field):
    if field.field.widget.__class__.__name__ is 'TextInput':
        return 'text'
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
    if field.field.widget.__class__.__name__ is 'CheckboxSelectMultiple':
        return 'cbselectm'
    if field.field.widget.__class__.__name__ is 'RadioSelect':
        return 'radio'
    if field.field.widget.__class__.__name__ is 'FileInput' \
        or field.field.widget.__class__.__name__ is 'ClearableFileInput':
        return 'file'
    if field.field.__class__.__name__ is 'DateField':
        return 'date'
    if field.field.__class__.__name__ is 'EmailField':
        return 'email'
    return 'default'


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
def cbselectm(field):
    return field.as_widget(attrs={'class': 'unstyled'})


@register.filter
def calendar(field):
    return field.as_widget(attrs={'class': 'input-small datepicker'})


from django import template


register = template.Library()


@register.filter
def active(name, request):
    if name in request.path:
        return 'active'
    return ''


@register.filter
def icon(field):
    try:
        if type(field) == 'password':
            return 'lock'
        if type(field) in ('text', 'date', 'choice', 'multiple_choice'):
            return 'pencil'
        if type(field) == 'email':
            return 'envelope'
    except:
        pass


@register.filter
def type(field):
    try:
        if field.field.widget.__class__.__name__ is 'Textarea':
            return 'textarea'
        if field.field.widget.__class__.__name__ is 'PasswordInput':
            return 'password'
        if field.field.__class__.__name__ is 'ModelChoiceField':
            return 'choice'
        if field.field.__class__.__name__ is 'ModelMultipleChoiceField':
            return 'multiple_choice'
        if field.field.__class__.__name__ is 'DateField':
            return 'date'
        if field.field.__class__.__name__ is 'EmailField':
            return 'email'
    except:
        pass
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

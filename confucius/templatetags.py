from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.filter
def active(request, name):
    try:
        if request.path == reverse(name):
            return 'active'
    except:
        pass

    return ''

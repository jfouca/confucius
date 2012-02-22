from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.filter
def active(name, request):
    try:
        if request.path.startswith(reverse(name)):
            return 'active'
    except:
        pass

    return ''

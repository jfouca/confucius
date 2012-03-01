from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect

from confucius.models import Conference, Membership


def role_required(test_func):
    def decorator(view_func):
        def inner_decorator(request, *args, **kwargs):
            pk = kwargs.pop('conference_pk', None)
            membership = None

            try:
                if pk is not None:
                    conference = Conference.objects.get(pk=pk)
                else:
                    conference = request.user.get_last_accessed_conference()
                membership = Membership.objects.get(user=request.user, conference=conference)
            except:
                pass

            if not membership or not test_func(membership):
                messages.warning(request, u'Unauthorized access.')
                return redirect('membership_list')

            membership.set_last_accessed()

            request.membership = membership
            request.conference = conference

            return view_func(request, *args, **kwargs)
        return wraps(view_func)(inner_decorator)
    return decorator


def has_chair_role(view_func):
    def has_chair_role(membership):
        return membership.has_chair_role()
    decorator = role_required(has_chair_role)
    return decorator(view_func)


def has_reviewer_role(view_func):
    def has_chair_role(membership):
        return membership.has_reviewer_role() or membership.has_chair_role()
    decorator = role_required(has_chair_role)
    return decorator(view_func)


def has_submitter_role(view_func):
    def has_chair_role(membership):
        return membership.has_submitter_role() or membership.has_chair_role()
    decorator = role_required(has_chair_role)
    return decorator(view_func)


def has_role(view_func):
    decorator = role_required(lambda m: True)
    return decorator(view_func)

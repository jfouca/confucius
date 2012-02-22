from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from confucius.models import Conference, ConferenceUserRole
from confucius.forms import EditConfForm

from confucius.decorators import user_access_conference


@login_required
@user_access_conference()
def home_conference(request):
    return HttpResponse('')
    """
    conference = Conference.objects.get(pk=1)
    directory = "conference/home/"

    if conference.president is request.user:
        roles = ()
        template = "conf_PRES.html"
        #Pour le livrable 3, voir 4, il faudra creer des listes d'evaluation, de soumissions et d'alertes
    else:
        roles = ConferenceUserRole.objects.get(conference=conference, user=request.user).role.all()
        template = "conf_AUTHREVI.html"

    return render_to_response(directory + template, {'conference': conference, 'roles': roles, 'rolesCode': [role.code for role in roles]}, context_instance=RequestContext(request))
    """


@login_required
@user_access_conference(nameKwargConfId='conf_id')
def change_conference(request, conf_id):
    return HttpResponse('')
    """
    conference = Conference.objects.get(pk=conf_id)
    account = User.objects.get(user=request.user)
    account.actual_conference = conference
    account.save()
    """

    return redirect('home_conference')


@login_required
@user_access_conference(onlyPresident=True)
def close_conference(request):
    return HttpResponse('')
    """
    account = Account.objects.get(user=request.user)
    conference = account.actual_conference

    if request.method == 'POST':
        conference.isOpen = False
        conference.save()
        return render_to_response('conference/confirm_close_conference.html', {'conference':conference}, context_instance=RequestContext(request))
    return render_to_response('conference/close_conference.html', {'conference':conference}, context_instance=RequestContext(request))
    """


@login_required
@user_access_conference(onlyPresident=True)
def open_conference(request):
    """
    account = Account.objects.get(user=request.user)
    conference = account.actual_conference

    if request.method == 'POST':
        conference.isOpen = True
        conference.save()
        return render_to_response('conference/confirm_open_conference.html', {'conference':conference}, context_instance=RequestContext(request))
    return render_to_response('conference/open_conference.html', {'conference':conference}, context_instance=RequestContext(request))
    """


@login_required
def list_conference(request):
    return HttpResponse('')
    """
    conferences_president = Conference.objects.filter(president=request.user).order_by('endConfDate')
    conferences_with_role = ConferenceUserRole.objects.filter(account=request.user).filter(conference__isOpen="True").order_by('conference__endConfDate')
    return render_to_response('conference/list_conference.html', { 'conferences_president' : conferences_president ,'conferences_with_role' : conferences_with_role }, context_instance=RequestContext(request))
    """


@login_required
@user_access_conference(onlyPresident=True)
def edit_conference(request):
    return HttpResponse('')
    """
    account = Account.objects.get(user=request.user)
    conference = account.actual_conference
    form = EditConfForm()

    if conference.president.user == request.user:
        auth = "true"
        print "is president"
        if request.POST:
            form = EditConfForm(request.POST, instance=conference)
            if form.is_valid():
                form.save()
        else:
            form = EditConfForm(instance=conference)

        return render_to_response("conference/edit_conference.html", {
        "auth": auth, "conf_id" : conference.pk , "form" : form, "conference" : conference
        },context_instance=RequestContext(request))

    else:
        auth = "false"
        return render_to_response("conference/edit_conference.html", {
        "conf_id" : conf_id , "auth" : auth, "conference" : conference
        },context_instance=RequestContext(request))

    auth = "true"
    return render_to_response("conference/edit_conference.html", {
    "auth": auth, "conf_id" : conf_id , "form" : form, "conference" : conference
    },context_instance=RequestContext(request))
    """

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from teamspirit.forms import TeamForm, SignUpForm
from teamspirit.models import Team
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate


def landing_page(request):
    context = {}
    context['teams'] = Team.objects.all().order_by('name')
    return render(request, 'teamspirit/landing.html', { "context" : context })


@login_required
def dashboard(request):
    context = {}
    context['teams'] = Team.objects.all().order_by('name')
    return render(request, 'teamspirit/dashboard.html', { "context" : context })

def sign_up(request):

    if request.method == 'POST': # If the form has been submitted...

        data = request.POST.copy()
        form = SignUpForm(data) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            #form.save()
            new_user = User.objects.create_user(form.cleaned_data['username'],
                                  form.cleaned_data['email'],
                                  form.cleaned_data['password'])
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name  = form.cleaned_data['last_name']
            new_user.save()
            auth_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password'],
                                    )
            login(request, auth_user)
            return redirect('landing_page')
        else:
            pass
    else:       
        form = SignUpForm() # An unbound form

    return render(request, 'teamspirit/signup.html', { "form" : form })

@login_required
def team_create(request):
    if request.method == 'POST': # If the form has been submitted...
        data = request.POST.copy()
        data['owner'] = request.user.id
        data.setlist( 'members', [request.user.id] )
        form = TeamForm(data) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save()
            return redirect('landing_page')
        else:
            pass
    else:
        form = TeamForm() # An unbound form

    return render(request, 'teamspirit/team_create.html', { "form" : form })

@login_required
def add_member(request, pk):
    team = Team.objects.get(id=pk)
    context = {}
    context['team'] = team
    context['users'] = User.objects.all().order_by('name')
    if request.method == 'POST': # If the form has been submitted...
        data = request.POST.copy()
        data['owner'] = team.owner.id
        data['name']  = team.name
        form = TeamForm(data, instance=team) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save()
            return redirect('landing_page')
        else:
            pass
    else:
        formData = {
            'members' : team.members,
        }
        form = TeamForm() # An unbound form

    return render(request, 'teamspirit/add_member.html', { "form" : form, 'context':context })

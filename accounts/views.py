from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from project.models import Project
from django.template.context import RequestContext
from django.views import generic
from accounts import forms
from accounts.models import UserProfile


# Create your views here.
# Pag for log in
def login(request):
    if request.user.is_authenticated():
        return redirect('/accounts/%s/' % request.user.id)
    else:
        if request.method == 'GET':
            form = forms.LoginForm
            return render_to_response('login.html', RequestContext(request, {'form': form,}))
        else:
            form = forms.LoginForm(request.POST)
            if form.is_valid():
                username = request.POST.get('username', '')
                password = request.POST.get('password', '')
                user = auth.authenticate(username=username, password=password)
                if user is not None and user.is_active:
                    auth.login(request, user)
                    return render_to_response('base.html', RequestContext(request))
                else:
                    return render_to_response('login.html',
                                              RequestContext(request, {'form': form, 'password_is_wrong': True}))
            else:
                return render_to_response('login.html', RequestContext(request, {'form': form,}))


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")


#Page for user info
@login_required(login_url='/accounts/login/')
def user_info_view(request):

    return render(request, "userinfo_view.html")

# class DetailView(generic.DetailView):
#     model = UserProfile
#     template_name = 'account/detail.html'



@login_required(login_url='/accounts/login/')
def user_project_list_view(request):
    response = "Hi. This is the project list page for user %s"
    username = request.user.get_username()
    return HttpResponse(response % username)


@login_required(login_url='/accounts/login/')
def user_project_detail_view(request, project_id):
    response = "Hi. This is the project %s page for user %s"
    username = request.user.get_username()
    project = Project.objects.get(pk=project_id)
    return HttpResponse(response % (project.name, username))


@login_required(login_url='/accounts/login/')
def user_credit_list_view(request):
    response = "Hi. This is the credit list page for user %s"
    username = request.user.get_username()
    return HttpResponse(response % username)

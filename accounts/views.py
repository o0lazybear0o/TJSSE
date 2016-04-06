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

                if username == '':
                    return render(request, 'login.html', {'form': form, 'username_not_valid': True})
                elif password == '':
                    return render(request, 'login.html', {'form': form, 'password_not_valid': True})

                user = auth.authenticate(username=username, password=password)

                if user is not None and user.is_active:
                    auth.login(request, user)
                    return render(request, 'base.html')
                else:
                    return render(request, 'login.html', {'form': form, 'password_is_wrong': True})
            else:
                return render(request, 'login.html', {'form': form, 'not_valid': True})


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")


# Change Password
@login_required
def change_password_view(request):
    if request.method == 'GET':
        form = forms.ChangePasswordForm
        return render(request, 'change_password.html', {'form': form,})
    else:
        form = forms.ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = request.POST.get('old_password', '')
            new_password = request.POST.get('new_password', '')
            new_password_again = request.POST.get('new_password_again', '')

            if old_password == "" or new_password == "" or new_password_again == "":
                return render(request, 'change_password.html', {'form': form, 'not_valid': True})

            username = request.user.username
            user = user = auth.authenticate(username=username, password=old_password)

            if user is not None and user.is_active:
                if new_password != new_password_again:
                    return render(request, 'change_password.html', {'form': form, 'password_not_same': True})
                else:
                    user.set_password(new_password)
                    user.save()
                    auth.login(request, user)
                return render(request, 'change_password.html', {'form': form, 'success': True})
            else:
                return render(request, 'change_password.html', {'form': form, 'old_password_is_wrong': True})
        else:
            return render(request, 'change_password.html', {'form': form, 'not_valid': True})

@login_required(login_url='/accounts/login/')
def new_project(request):
    return render(request, 'new_project.html')

# Page for user info
@login_required(login_url='/accounts/login/')
def change_user_info_view(request):
    if request.method == 'GET':
        form = forms.ChangeStudentInfoForm()
        return render(request, 'userinfo_change.html', {'form': form,})
    else:
        form = forms.ChangeStudentInfoForm(request.POST)
        if form.is_valid():
            old_password = request.POST.get('grade', '')
            new_password = request.POST.get('major', '')
            new_password_again = request.POST.get('phone', '')
            return render(request, 'userinfo_change.html', {'form': form, 'success': True})


@login_required(login_url='/accounts/login/')
def user_info_view(request):

    return render(request, "userinfo_view.html")


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
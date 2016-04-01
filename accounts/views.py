from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from project.models import Project


# Create your views here.
#Pag for log in
def login(request):
    if request.user.is_authenticated():
        return redirect('/accounts/%s/' %request.user.id)
    else :
        return HttpResponse("Hi. This is the page for login")

#Page for user info
@login_required(login_url='/accounts/login/')
def user_info_view(request):
    response = "Hi. This is the info page for user %s"
    username = request.user.get_username()
    return HttpResponse(response % username)

@login_required(login_url='/accounts/login/')
def user_project_list_view(request):
    response = "Hi. This is the project list page for user %s"
    username = request.user.get_username()
    return HttpResponse(response % username)

@login_required(login_url='/accounts/login/')
def user_project_detail_view(request, project_id):
    response = "Hi. This is the project %s page for user %s"
    username = request.user.get_username()
    project = Project.objects.get(pk = project_id)
    return HttpResponse(response % (project.name, username))

@login_required(login_url='/accounts/login/')
def user_credit_list_view(request):
    response = "Hi. This is the credit list page for user %s"
    username = request.user.get_username()
    return HttpResponse(response % username)

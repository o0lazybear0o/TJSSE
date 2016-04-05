from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Project
# Create your views here.

@login_required(login_url='/accounts/login/')
def project_list_view(request):
    return HttpResponse("Hello. You're at the project list page.")

@login_required(login_url='/accounts/login/')
def project_detail_view(request, project_id):
    project = Project.objects.get(pk = project_id)
    return HttpResponse("Hello. You're at the project %s page." % project.name)
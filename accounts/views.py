from django.http import HttpResponse
from .models import CustomUser


# Create your views here.
def login(request):
    return HttpResponse("Hi. This is the page for login")


def userinfo(request, user_id):
    response = "Hi. This is the page for user %s"
    user = CustomUser.objects.get(pk=user_id)
    username = user.get_username()
    return HttpResponse(response % username)

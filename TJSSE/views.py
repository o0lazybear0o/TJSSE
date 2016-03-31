from django.http import HttpResponse


def homepage(request):
    return HttpResponse("Hello. You're at the TJSSE homepage.")
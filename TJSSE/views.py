from django.http import HttpResponse
from django.shortcuts import render


def homepage(request):
    # return HttpResponse("Hello. You're at the TJSSE homepage.")
    return render(request, "base.html")
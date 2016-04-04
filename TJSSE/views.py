from django.http import HttpResponse
from django.shortcuts import render


def homepage(request):
<<<<<<< HEAD
=======
    # return HttpResponse("Hello. You're at the TJSSE homepage.")
>>>>>>> 431169f1fd451e3c16daf7fdb99a7ea545b4b772
    return render(request, "base.html")
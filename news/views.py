from django.http import HttpResponse
from .models import News


def news_list_view(request):
    return HttpResponse("Hello. You're at the news list page.")

def news_detail_view(request, news_id):
    news = News.objects.get(pk = news_id)
    return HttpResponse("Hello. You're at the news %s page." % news.title)
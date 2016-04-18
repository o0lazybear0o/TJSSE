from django.http import HttpResponse
from .models import News,Attachment
from django.shortcuts import redirect, render, render_to_response
from django.db.models import Q
from .forms import SearchForm

def news_list_view(request):
    news_list=News.objects.filter(status=News.STATUS_PASS)
    search_form=SearchForm()
    return render(request,'news/news_list.html',{'news_list':news_list,\
                                                 'form':search_form})

def news_search_list_view(request):
    search_infor=getSearchInfor(request)

    if search_infor!=None and search_infor[0]!='':
        news_list=News.objects.filter(Q(title__contains=search_infor[0])&\
                                      Q(status=News.STATUS_PASS))
        search_form=SearchForm()

        return render(request,'news/news_list.html',{'news_list':news_list,\
                                                     'form':search_form})
    else:
        return news_list_view(request)

def news_detail_view(request, news_id):
    news = News.objects.get(pk = news_id)
    attachment_list=Attachment.objects.filter(news=news)
    detail_att_list=[attchment.filepath for attchment in attachment_list]
    search_form = SearchForm()

    return render(request,'news/news_detail.html',{'news':news,\
                                                   'detail_att_list':detail_att_list,\
                                                   'form':search_form})

def getSearchInfor(request):
    search_form=SearchForm(request.POST)
    if search_form.is_valid():
        search_val=request.POST['search_val']
        return [search_val]
    else:
        return None
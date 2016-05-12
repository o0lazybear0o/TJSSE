from django.http import HttpResponse
from .models import News,Attachment
from django.shortcuts import redirect, render, render_to_response
from django.db.models import Q
from .forms import SearchForm
from TJSSE.utils import ExtendPaginator
from django.core.paginator import PageNotAnInteger, EmptyPage

PAGE_LIMIT = 3

def news_list_view(request):
    news_list=News.objects.filter(status=News.STATUS_PASS)
    search_form=SearchForm()

    paginator = ExtendPaginator(news_list, PAGE_LIMIT)
    page_id = request.GET.get('page')
    try:
        news_list = paginator.page(page_id)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        news_list = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        news_list = paginator.page(paginator.num_pages)  # 取最后一页的记录

    return render(request,'news/news_list.html',{'news_list':news_list,\
                                                 'form':search_form})

def news_search_list_view(request):
    search_infor=getSearchInfor(request)

    if search_infor!=None and search_infor['search_val']!='':
        news_list=News.objects.filter(Q(title__contains=search_infor['search_val'])&\
                                      Q(status=News.STATUS_PASS))
        search_form=SearchForm()

        paginator = ExtendPaginator(news_list, PAGE_LIMIT)
        page_id = request.GET.get('page')
        try:
            news_list = paginator.page(page_id)  # 获取某页对应的记录
        except PageNotAnInteger:  # 如果页码不是个整数
            news_list = paginator.page(1)  # 取第一页的记录
        except EmptyPage:  # 如果页码太大，没有相应的记录
            news_list = paginator.page(paginator.num_pages)  # 取最后一页的记录

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
        search_val=request.GET['search_val']
        return {'search_val':search_val}
    else:
        return None
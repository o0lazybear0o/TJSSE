from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.news_list_view,name='news_list'),
    url(r'^search$',views.news_search_list_view ,name='new_search_list'),
    url(r'^(?P<news_id>[0-9]+)/$', views.news_detail_view, name='news_detail'),
]
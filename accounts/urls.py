from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$', views.login,name='login'),
    url(r'^info/$', views.user_info_view, name='user_info'),
    url(r'^project/$', views.user_project_list_view, name='user_project_list'),
    url(r'^project/(?P<project_id>[0-9]+)/$', views.user_project_detail_view, name='user_project_detail'),
    url(r'^credit/$', views.user_credit_list_view, name='user_credit_list'),
]
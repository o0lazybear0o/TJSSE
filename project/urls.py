from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.project_list_view,name='project_list'),
    url(r'^(?P<project_id>[0-9]+)/$', views.project_detail_view, name='project_detail'),
]
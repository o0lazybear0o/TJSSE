from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^new_student/$', views.new_student),
    url(r'^new_professor/$', views.new_professor),
    url(r'^project_type/$', views.project_type),
    url(r'^new_news/$', views.new_news),
    url(r'^change_project_status/$', views.change_project_status),
]

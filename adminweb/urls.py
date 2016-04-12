from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^new_student/$', views.new_student),
    url(r'^new_professor/$', views.new_professor),
    url(r'^project_type/$', views.project_type),
    url(r'^new_news/$', views.new_news),
    url(r'^change_project_status/$', views.change_project_status),
    url(r'^change_credit_status/(?P<status>[0-9]+)$', views.change_credit_statu, name='change_credit_stauts'),
    url(r'^super_delete_credit/(?P<id>[0-9]+)$', views.super_delete_credit, name='super_delete_credit'),
    url(r'^super_edit_credit/(?P<id>[0-9]+)$', views.super_edit_credit, name='super_edit_credit'),
    url(r'^get_student_credit(?P<id>[0-9]+)/(?P<status>[0-9]+)$', views.get_student_credit, name='get_student_credit'),
]

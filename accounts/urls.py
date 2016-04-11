from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^info/$', views.user_info_view, name='user_info'),
    url(r'^new_project/$', views.new_project, name='new_project'),
    url(r'^my_project/$', views.my_project, name='my_project'),

    url(r'^my_credit/$', views.user_credit_list_view, name='user_credit_list'),
    url(r"^new_credit/$", views.new_credit, name='new_credit'),
    url(r'^edit_credit/(?P<id>[0-9]+)$', views.edit_credit, name='edit_credit'),
    url(r'^delete_credit/(?P<id>[0-9]+)$', views.delete_credit, name='delete_credit'),

    url(r'^info/change_info/$', views.change_user_info_view, name='change_user_info'),
    url(r'^info/change_password/$', views.change_password_view, name='change_password'),

    url(r'^adminweb/', include('adminweb.urls'))
]
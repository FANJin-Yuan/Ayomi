from django.urls import re_path, path
from FirstApp import views

app_name = 'FirstApp'

urlpatterns = [
    re_path(r'^register/$', views.register, name='register'),
    re_path(r'^login/$', views.login, name='login'),
    re_path(r'^user/(?P<pk>\d+)/profile/$', views.profile, name='profile'),
    # re_path(r'^user/(?P<pk>\d+)/profile/update/$', views.profile_update, name='profile_update'),
    re_path(r"^logout/$", views.logout, name='logout'),
    path('index/', views.index),
]
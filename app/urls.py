from django.contrib import admin
from django.urls import path, include

from . import views
from django.views.generic import TemplateView
urlpatterns = [

    path('',views.home, name = "home"),
    path('register',views.register, name = "register"),
    path('login', views.log_in, name="login"),
    path('logout', views.logout, name="logout"),
    path('prepython', views.prepython, name="prepython"),
    path('stream', views.stream_video, name='stream_video'),
    path('webcam', views.webcam, name='webcam'),
    path('interview', views.interview, name='interview'),
    path('frame_generator', views.frame_generator, name='frame_generator'),

]
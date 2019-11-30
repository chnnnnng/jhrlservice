from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('getStart',views.getStart),
    path('login',views.login),
    path('getYzm', views.getYzm),
    path('getSettings',views.getSettings),
    path('getKb',views.getKb),
]
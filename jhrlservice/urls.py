from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('jhrlapis/', include('jhrlapis.urls')),
]
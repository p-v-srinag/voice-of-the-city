# core/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),               # HTML form UI
    path('voice/', views.handle_voice, name='voice') # JSON API
]

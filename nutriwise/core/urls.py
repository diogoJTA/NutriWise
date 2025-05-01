from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.main, name='main'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('scan/', views.scan, name='scan')
]
from django.urls import path
from . import views
urlpatterns = [
    path('send/', views.send_newsletter, name='send_newsletter'),
]
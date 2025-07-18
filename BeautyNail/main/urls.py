from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello_customers, name='main'),
    path('about', views.views_about, name='about'),
]
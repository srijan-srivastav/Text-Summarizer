from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home,name = 'home-page'),
    path('ans/', views.ans, name = 'sum-page'),
]
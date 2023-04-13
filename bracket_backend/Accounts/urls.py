from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
  path('signup/', views.SignUp), 
  path("login/", views.Login), 
  path("profile/", views.UserApi), 
  path('logout/', views.LogOut), 
]

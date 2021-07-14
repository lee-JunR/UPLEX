from django.contrib import admin
from django.urls import path, include
from accounts.views import login, signup

urlpatterns = [
    path('login/',login),
    path('signup/',signup),
]

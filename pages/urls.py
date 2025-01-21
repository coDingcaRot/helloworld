# pages/urls.py
# URLS that we use to fetch for linking between pages
from django.urls import path, include
from .views import homePageView, aboutPageView, jonathanielPageView, results, homePost, todos, register, message, logoutView, secretArea
import pandas as pd

urlpatterns = [
    path('', homePageView, name='home'),
    path('about/', aboutPageView, name='about'),
    path('jonathaniel/', jonathanielPageView, name='jonathaniel'),
    path('homePost/', homePost, name='homePost'),
    path('<int:choice>/results/', results, name='results'),
    path('results/<int:choice>/<str:gmat>/', results, name='results'),
    path('todos', todos, name='todos'),
    path("register/", register, name="register"),  # <-- added Lab 3
    path('message/<str:msg>/<str:title>/', message, name="message"),  # <-- added lab 3
    path('', include("django.contrib.auth.urls")),  # <-- added lab 3
    path("logout/", logoutView, name="logout"), # <-- Added lab 3
    path("secret/", secretArea, name="secret")
]

# pages/urls.py
from django.urls import path
from .views import homePageView, aboutPageView, jonathanielPageView, results, homePost
import pandas as pd

urlpatterns = [
    path('', homePageView, name='home'),
    path('about/', aboutPageView, name='about'),
    path('jonathaniel/', jonathanielPageView, name='jonathaniel'),
    path('homePost/', homePost, name='homePost'),
    path('<int:choice>/results/', results, name='results'),
    path('results/<int:choice>/<str:gmat>/', results, name='results'),
]

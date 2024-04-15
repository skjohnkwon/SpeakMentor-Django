# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('search', views.search, name='search'),
    path('process', views.process, name='process')
]

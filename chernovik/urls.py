"""
URL configuration for chernovik project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import chernovik
from . import views
from django.contrib.auth import views as auth_views
# from .views import places_map

app_name = 'chernovik'

urlpatterns = [
    path('place/<str:place_id>/', views.place_detail, name='place_detail'),
    path('vote/', views.vote_comment, name='chernovik_vote_comment'),

    path('places_map/', views.places_map, name='places_map'),
    # path('', places_map, name='places_map'),
]

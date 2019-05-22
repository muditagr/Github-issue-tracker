from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url('track/', views.Track.as_view(), name="gh-tracker"),
]
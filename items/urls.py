from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
    path('', views.ItemsView.as_view(), name="items"),
    path('new/', views.NewView.as_view(), name="new"),
]

from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
    path('', views.ProjectsView.as_view(), name="projects"),
    path('new/', views.NewProjectView.as_view(), name="new_project"),
]

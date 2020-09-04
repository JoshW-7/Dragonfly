from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
    path('', views.ProjectsView.as_view(), name="projects"),
    path('project/', views.ProjectDetailView.as_view(), name="new_project"),
    path('project/<int:pk>/', views.ProjectDetailView.as_view(), name="project"),
]

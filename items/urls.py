from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
    path('', views.ItemsView.as_view(), name="items"),
    path('item/', views.ItemDetailView.as_view(), name="new_item"),
    path('item/<int:pk>/', views.ItemDetailView.as_view(), name="item"),
    path('item/<str:id>/resolve', views.resolve, name="resolve"),
    path('item/<str:id>/unresolve', views.unresolve, name="unresolve"),
    path('item/<str:id>/remove', views.remove, name="remove"),
    path('item/<str:id>/remove_file', views.remove_file, name="remove_file"),
    path('item/<str:id>/upload', views.upload, name="upload"),
    path('item/<str:id>/comment', views.comment, name="comment"),
]

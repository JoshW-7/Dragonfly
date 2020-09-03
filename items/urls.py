from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
    path('', views.ItemsView.as_view(), name="items"),
    path('item/', views.ItemDetailView.as_view(), name="new_item"),
    path('item/<int:pk>/', views.ItemDetailView.as_view(), name="item"),
    path('remove/<str:id>', views.remove, name="remove"),
    path('resolve/<str:id>', views.resolve, name="resolve"),
    path('unresolve/<str:id>', views.unresolve, name="unresolve"),
]

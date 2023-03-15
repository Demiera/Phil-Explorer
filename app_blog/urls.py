from django.urls import path
from . import views



urlpatterns = [
    # blog-deleted
    path('deleted/', views.BlogDeletedListView.as_view(), name='blog-list-deleted'),
    path('deleted/<str:pk>', views.BlogRestoreView.as_view(), name='blog-restore-deleted'),
    # blog
    path('', views.BlogListView.as_view(), name='blog-list'),
    path('<str:title>', views.BlogDeleteView.as_view(), name='blog-detail'),
]
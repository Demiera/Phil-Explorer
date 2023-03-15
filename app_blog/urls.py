from django.urls import path
from . import views

urlpatterns = [
    # blog-deleted
    path('blog-deleted/', views.BlogDeletedListView.as_view(), name='blog-list-deleted'),
    path('blog-deleted/<str:pk>', views.BlogRestoreView.as_view(), name='blog-restore-deleted'),
    # blog
    path('blog/', views.BlogListView.as_view(), name='blog-list'),
    path('blog/<str:title>', views.BlogDeleteView.as_view(), name='blog-detail'),
]
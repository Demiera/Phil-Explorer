from django.urls import path
from . import views

urlpatterns = [
    # Published
    path('', views.BlogListView.as_view(), name='blog-list'),
    path('<slug:slug>/', views.BlogDeleteView.as_view(), name='blog-detail'),

    # Drafts
    path('drafts/', views.BlogDraftView.as_view(), name='blog-draft-list'),
    path('draft/<slug:slug>/', views.BlogDraftRetrieveView.as_view(), name='blog-draft-detail'),

    # Deleted / restore
    path('deleted/', views.BlogDeletedListView.as_view(), name='blog-deleted-list'),
    path('restore/<slug:slug>/', views.BlogRestoreView.as_view(), name='blog-restore-deleted'),
]
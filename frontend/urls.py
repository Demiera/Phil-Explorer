from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_published, name='dashboard'),
    path('drafts/', views.dashboard_drafts, name='drafts'),
    path('deleted/', views.dashboard_deleted, name='deleted'),
    path('create/', views.create_post, name='create-post'),
    path('edit/<slug:slug>/', views.edit_post, name='edit-post'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login_view, name='login-page'),
    path('register/', views.register_view, name='register-page'),
]
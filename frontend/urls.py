from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('blogs/', views.blog_list, name='blog-list-page'),
    path('blogs/<slug:slug>/', views.blog_detail, name='blog-detail-page'),
    path('login/', views.login_view, name='login-page'),
    path('register/', views.register_view, name='register-page'),
]
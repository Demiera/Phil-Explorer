from django.urls import path
from . import views

urlpatterns = [
    path('', views.SearchListBlog.as_view(), name='blog-search'),
]
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def login_view(request):
    return render(request, 'frontend/login.html')

def register_view(request):
    return render(request, 'frontend/register.html')

def dashboard_published(request):
    return render(request, 'frontend/dashboard_published.html')

def dashboard_drafts(request):
    return render(request, 'frontend/dashboard_drafts.html')

def dashboard_deleted(request):
    return render(request, 'frontend/dashboard_deleted.html')

def create_post(request):
    return render(request, 'frontend/create_post.html')

def edit_post(request, slug):
    return render(request, 'frontend/edit_post.html', {'slug': slug})

def profile(request):
    return render(request, 'frontend/profile.html')
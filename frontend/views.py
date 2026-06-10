from django.shortcuts import render

def landing(request):
    return render(request, 'frontend/landing.html')

def blog_list(request):
    return render(request, 'frontend/blog_list.html')

def blog_detail(request, slug):
    return render(request, 'frontend/blog_detail.html', {'slug': slug})

def login_view(request):
    return render(request, 'frontend/login.html')

def register_view(request):
    return render(request, 'frontend/register.html')
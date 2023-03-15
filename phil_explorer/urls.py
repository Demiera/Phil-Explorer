from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('app_user.urls')),
    path('api/blog/', include('app_blog.urls')),
    path('api/blog/search/', include('blog_search.urls')),
]

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),
    path('api/', include('app_user.urls')),

    # ⚠️  blog/search/ MUST come before blog/ so Django doesn't
    #     swallow "search" as a slug in app_blog's <slug:slug> pattern
    path('api/blog/search/', include('blog_search.urls')),
    path('api/blog/', include('app_blog.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
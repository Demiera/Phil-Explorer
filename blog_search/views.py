from rest_framework import generics
from app_blog.models import Blog, BlogManager
from app_blog.serializers import BlogSerializer

class SearchListBlog(generics.ListAPIView):
    queryset = Blog.objects.filter(is_deleted=False)
    serializer_class = BlogSerializer

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        q = self.request.GET.get('q')
        result = Blog.objects.none()
        if q is not None:
            result = BlogManager(Blog).search(q)
        return result
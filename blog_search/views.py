from rest_framework import generics, permissions
from app_blog.models import Blog, BlogManager
from app_blog.serializers import BlogSerializer


class IsAuthenticatedOrQueryParamsAllowed(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        else:
            return request.GET.get('filter') is None

class SearchListBlog(generics.ListAPIView):
    queryset = Blog.objects.filter(is_deleted=False)
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrQueryParamsAllowed]

    def get_queryset(self, result=None, *args, **kwargs):
        qs = BlogManager(Blog)
        q = self.request.GET.get('q')
        date_by = self.request.GET.get('filter')
        if q is not None:
            result = qs.search(q)
        else:
            result = Blog.objects.none()
        if self.request.user.is_authenticated and date_by is not None:
            if date_by == 'latest':
                result = result.order_by('-date_created')
            elif date_by == 'oldest':
                result = result.order_by('date_created')
        return result

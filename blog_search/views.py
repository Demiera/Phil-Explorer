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

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        q = self.request.GET.get('q')
        date_by = self.request.GET.get('filter')
        draft = self.request.GET.get('draft')

        if q is not None:
            qs = qs.search(q)
        if self.request.user.is_authenticated and date_by is not None:
            if date_by == 'latest':
                qs = qs.order_by('-date_created')
            elif date_by == 'oldest':
                qs = qs.order_by('date_created')
            if draft is not None and draft.lower() == 'false':
                qs = qs.filter(published=False)
            elif draft is not None and draft.lower() == 'true':
                qs = qs.filter(published=True)
        return qs



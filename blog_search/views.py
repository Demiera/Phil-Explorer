from rest_framework import generics, permissions
from app_blog.models import Blog
from app_blog.serializers import BlogSerializer

class IsAuthenticatedOrQueryParamsAllowed(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        else:
            return request.GET.get('filter') is None \
                and request.GET.get('draft') is None \
                and request.GET.get('deleted') is None

class SearchListBlog(generics.ListAPIView):
    queryset = Blog.objects.filter(is_deleted=False)
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrQueryParamsAllowed]

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        q = self.request.GET.get('q')
        date_by = self.request.GET.get('filter')
        draft = self.request.GET.get('draft')
        deleted = self.request.GET.get('deleted')

        if q is not None:
            qs = qs.search(q)
        if self.request.user.is_authenticated and deleted is not None:
            if deleted.lower() == 'true':
                qs = Blog.objects.filter(is_deleted=True)

        if self.request.user.is_authenticated and date_by is not None:
            if date_by == 'latest':
                qs = qs.order_by('-date_created')
            elif date_by == 'oldest':
                qs = qs.order_by('date_created')

        if self.request.user.is_authenticated and draft is not None:
            if draft.lower() == 'false':
                qs = qs.filter(published=False)
            elif draft.lower() == 'true':
                qs = qs.filter(published=True)

        return qs

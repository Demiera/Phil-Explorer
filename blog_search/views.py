from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db.models import Q
from app_blog.models import Blog
from app_blog.serializers import BlogSerializer, BlogDraftSerializer, BlogDeletedSerializer


class BlogSearchPermission(permissions.BasePermission):
    """
    - Authenticated users: full access (published, drafts, deleted).
    - Unauthenticated users: only public published posts (no ?published,
      ?filter, or ?deleted params allowed).
    """
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True
        return (
            request.GET.get('published') is None
            and request.GET.get('filter') is None
            and request.GET.get('deleted') is None
        )


class BlogSearchPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'limit'
    max_page_size = 100

    def paginate_queryset(self, queryset, request, view=None):
        self.limit  = int(request.query_params.get('limit', self.page_size))
        self.offset = int(request.query_params.get('offset', 0))
        self.count  = queryset.count()
        self.request = request
        return list(queryset[self.offset: self.offset + self.limit])

    def get_paginated_response(self, data):
        return Response({'count': self.count, 'results': data})


class SearchListBlog(generics.ListAPIView):
    # Override the global IsAuthenticated default from settings.py
    permission_classes = [BlogSearchPermission]
    pagination_class   = BlogSearchPagination

    def get_serializer_class(self):
        deleted   = self.request.GET.get('deleted', 'false').lower()
        published = self.request.GET.get('published', 'true').lower()
        if deleted == 'true':
            return BlogDeletedSerializer
        if published == 'false':
            return BlogDraftSerializer
        return BlogSerializer

    def get_queryset(self):
        q         = self.request.GET.get('q', '').strip()
        date_by   = self.request.GET.get('filter', 'latest')
        published = self.request.GET.get('published')
        deleted   = self.request.GET.get('deleted', 'false')

        # Base queryset
        if self.request.user.is_authenticated and deleted == 'true':
            qs = Blog.objects.filter(is_deleted=True)
        else:
            qs = Blog.objects.filter(is_deleted=False)

        # Published filter
        if self.request.user.is_authenticated and published is not None:
            qs = qs.filter(published=(published.lower() == 'true'))
        else:
            qs = qs.filter(published=True)

        # Search
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))

        # Ordering
        qs = qs.order_by('date_created' if date_by == 'oldest' else '-date_created')

        return qs
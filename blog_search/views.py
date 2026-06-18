from rest_framework import generics, permissions
from app_blog.models import Blog
from app_blog.serializers import BlogSerializer


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Unauthenticated users may only hit the search endpoint without
    the 'published', 'filter', or 'deleted' params (i.e. plain public search).
    All authenticated users are allowed through unconditionally.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return (
            request.GET.get('published') is None
            and request.GET.get('filter') is None
            and request.GET.get('deleted') is None
        )


class SearchListBlog(generics.ListAPIView):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        q         = self.request.GET.get('q')
        date_by   = self.request.GET.get('filter')
        published = self.request.GET.get('published')   # 'true' | 'false' | None
        deleted   = self.request.GET.get('deleted')     # 'true' | None

        # ── base queryset ───────────────────────────────────────────────────
        if self.request.user.is_authenticated and deleted == 'true':
            qs = Blog.objects.filter(is_deleted=True)
        else:
            qs = Blog.objects.filter(is_deleted=False)

        # ── published filter ────────────────────────────────────────────────
        if self.request.user.is_authenticated and published is not None:
            if published.lower() == 'true':
                qs = qs.filter(published=True)
            elif published.lower() == 'false':
                qs = qs.filter(published=False)
        else:
            # Default: only show published posts to everyone (including
            # unauthenticated visitors and dashboard calls that omit the param).
            qs = qs.filter(published=True)

        # ── full-text search ────────────────────────────────────────────────
        if q:
            qs = qs.search(q)

        # ── ordering ────────────────────────────────────────────────────────
        if date_by == 'oldest':
            qs = qs.order_by('date_created')
        else:
            # 'latest' or no param → newest first (matches model Meta default)
            qs = qs.order_by('-date_created')

        return qs
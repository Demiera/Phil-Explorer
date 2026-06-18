from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Blog
from rest_framework import generics, permissions, status
from .serializers import BlogSerializer, BlogDeletedSerializer, BlogDraftSerializer


# ── Blog Published ───────────────────────────────────────────────────────────
class BlogListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Blog.objects.filter(is_deleted=False, published=True)
    serializer_class = BlogSerializer


class BlogDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Blog.objects.filter(is_deleted=False, published=True)
    serializer_class = BlogSerializer
    lookup_field = 'slug'

    def delete(self, request, *args, **kwargs):
        blog = self.get_object()
        blog.delete()  # soft delete via model's delete()
        return Response(
            {'message': f'"{blog.title}" has been moved to trash.'},
            status=status.HTTP_200_OK
        )


# ── Blog Draft ───────────────────────────────────────────────────────────────
class BlogDraftView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Blog.objects.filter(is_deleted=False, published=False)
    serializer_class = BlogDraftSerializer
    lookup_field = 'slug'


class BlogDraftRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Blog.objects.filter(is_deleted=False, published=False)
    serializer_class = BlogDraftSerializer
    lookup_field = 'slug'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if serializer.validated_data.get('published'):
            return Response({'message': 'This blog has been published.'}, status=status.HTTP_200_OK)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        blog = self.get_object()
        blog.delete()  # soft delete
        return Response(
            {'message': f'"{blog.title}" has been moved to trash.'},
            status=status.HTTP_200_OK
        )


# ── Blog Deleted / Restore ───────────────────────────────────────────────────
class BlogDeletedListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Blog.objects.filter(is_deleted=True)
    serializer_class = BlogDeletedSerializer


class BlogRestoreView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Blog.objects.filter(is_deleted=True)
    serializer_class = BlogDeletedSerializer
    lookup_field = 'slug'

    def put(self, request, *args, **kwargs):
        """Restore a soft-deleted post."""
        instance = self.get_object()
        instance.restore()
        return Response(
            {'message': f'"{instance.title}" has been restored.'},
            status=status.HTTP_200_OK
        )

    # Also handle PATCH in case DRF routes partial updates here
    def patch(self, request, *args, **kwargs):
        return self.put(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Permanently delete a post."""
        instance = self.get_object()
        instance.delete(hard=True)
        return Response(
            {'message': 'Post has been permanently deleted.'},
            status=status.HTTP_200_OK  # 200 so JS can read the response body
        )
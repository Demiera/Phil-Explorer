from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import Blog
from rest_framework import generics, permissions, status
from .serializers import BlogSerializer, BlogDeletedSerializer


class BlogListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Blog.objects.filter(is_deleted=False)
    serializer_class = BlogSerializer


class BlogDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Blog.objects.filter(is_deleted=False)
    serializer_class = BlogSerializer
    lookup_field = 'slug'

    def get_object(self):
        queryset = self.get_queryset()
        slug = self.kwargs.get('slug')
        obj = get_object_or_404(queryset, slug=slug)
        return obj


class BlogDeletedListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Blog.objects.filter(is_deleted=True)
    serializer_class = BlogDeletedSerializer


class BlogRestoreView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Blog.objects.filter(is_deleted=True)
    serializer_class = BlogDeletedSerializer
    lookup_field = 'slug'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete(hard=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.restore()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

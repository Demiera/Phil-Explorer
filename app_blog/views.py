from rest_framework.response import Response
from .models import Blog
from rest_framework import generics, permissions
from .serializers import BlogSerializer, BlogDeletedSerializer


class BlogListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Blog.objects.filter(is_deleted=False)
    serializer_class = BlogSerializer


class BlogDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Blog.objects.filter(is_deleted=False)
    serializer_class = BlogSerializer
    lookup_field = 'title'


class BlogDeletedListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Blog.objects.filter(is_deleted=True)
    serializer_class = BlogDeletedSerializer


class BlogRestoreView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Blog.objects.filter(is_deleted=True)
    serializer_class = BlogDeletedSerializer

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.restore()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)




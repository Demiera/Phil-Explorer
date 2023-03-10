from rest_framework.response import Response
from .models import Blog
from rest_framework import generics, viewsets
from .serializers import BlogSerializer, BlogDeletedSerializer


class BlogListView(generics.ListCreateAPIView):
    queryset = Blog.objects.filter(is_deleted=False)
    serializer_class = BlogSerializer



class BlogDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.filter(is_deleted=False)
    serializer_class = BlogSerializer



class BlogDeletedListView(generics.ListAPIView):
    queryset = Blog.objects.filter(is_deleted=True)
    serializer_class = BlogDeletedSerializer


class BlogRestoreView(generics.RetrieveUpdateAPIView):
    queryset = Blog.objects.filter(is_deleted=True)
    serializer_class = BlogDeletedSerializer

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.restore()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import Blog
from rest_framework import generics, permissions, status
from .serializers import BlogSerializer, BlogDeletedSerializer, BlogDraftSerializer


# Blog Published
class BlogListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Blog.objects.filter(is_deleted=False).filter(published=True)
    serializer_class = BlogSerializer

class BlogDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Blog.objects.filter(is_deleted=False).filter(published=True)
    serializer_class = BlogSerializer
    lookup_field = 'slug'

    def get_object(self):
        queryset = self.get_queryset()
        slug = self.kwargs.get('slug')
        obj = get_object_or_404(queryset, slug=slug)
        return obj

    def delete(self, request, *args, **kwargs):
        blog = self.get_object()
        response_data = {}
        if not blog.is_deleted:
            blog.delete()
            response_data['Message'] = f"{blog.title} has been moved to trash."
            return Response(response_data, status=status.HTTP_200_OK)

# Blog Draft
class BlogDraftView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Blog.objects.filter(is_deleted=False).filter(published=False)
    serializer_class = BlogDraftSerializer
    lookup_field = 'slug'

class BlogDraftRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Blog.objects.filter(is_deleted=False).filter(published=False)
    serializer_class = BlogDraftSerializer
    lookup_field = 'slug'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Check if the blog is published after update
        if serializer.validated_data.get('published'):
            return Response({'message': 'This blog has been published.'}, status=status.HTTP_200_OK)

        return Response(serializer.data)

# Blog Soft Delete
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
        message = f"data has been permanently deleted."
        return Response({'Message': message}, status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.restore()
        serializer = self.get_serializer(instance)
        message = f"{serializer.data['title']} has been restored."
        return Response({'Message': message})

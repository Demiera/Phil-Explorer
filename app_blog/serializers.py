from rest_framework import serializers
from .models import Blog


class BlogSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='blog-detail', lookup_field='slug')

    class Meta:
        model = Blog
        fields = [
            'url',
            'id',
            'title',
            'image',
            'description',
            'date_updated',
            'date_created',
            'published',
            'date_published',
        ]
        read_only_fields = [
            'date_created',
            'date_published',
            'date_updated',
        ]


class BlogDraftSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='blog-draft-detail', lookup_field='slug')

    class Meta:
        model = Blog
        fields = [
            'url',
            'id',
            'title',
            'image',
            'description',
            'published',
            'date_created',
            'date_published',
        ]
        read_only_fields = [
            'date_created',
            'date_published',
        ]

class BlogDeletedSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='blog-restore-deleted', lookup_field='slug')

    class Meta:
        model = Blog
        fields = [
            'url',
            'id',
            'title',
            'image',
            'description',
            'date_deleted',
            'is_deleted',
        ]

        read_only_fields = [
            'url',
            'id',
            'title',
            'image',
            'description',
            'date_deleted',
        ]

from rest_framework import serializers
from .models import Blog


class BlogSerializer(serializers.ModelSerializer):
    date_updated = serializers.ReadOnlyField()
    date_created = serializers.ReadOnlyField()
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

from rest_framework import serializers
from .models import Blog


class BlogSerializer(serializers.ModelSerializer):
    date_updated = serializers.ReadOnlyField()
    date_created = serializers.ReadOnlyField()
    url = serializers.HyperlinkedIdentityField(view_name='blog-detail', lookup_field='title')

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

    class Meta:
        model = Blog
        fields = [
            'id',
            'title',
            'image',
            'description',
            'date_deleted',
            'is_deleted',
        ]

        read_only_fields = [
            'id',
            'title',
            'image',
            'description',
            'date_deleted',
        ]

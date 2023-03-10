from rest_framework import serializers
from .models import Blog


class BlogSerializer(serializers.ModelSerializer):
    date_updated = serializers.ReadOnlyField()
    date_created = serializers.ReadOnlyField()
    date_deleted = serializers.ReadOnlyField()
    is_deleted = serializers.ReadOnlyField()

    class Meta:
        model = Blog
        fields = [
            'id',
            'title',
            'image',
            'description',
            'date_updated',
            'date_created',
            'date_deleted',
            'is_deleted',
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

from django.conf import settings
from rest_framework import serializers
from .models import Blog

MAX_BLOG_LENGTH = settings.MAX_BLOG_LENGTH
BLOG_ACTION_OPTIONS = settings.BLOG_ACTION_OPTIONS

class BlogActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)

    def validate_action(self, value):
        value = value.lower().strip() # "Like " -> "like"
        if not value in BLOG_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not a valid action for blogs")
        return value


class BlogCreateSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Blog
        fields = ['id', 'content', 'likes']

    def get_likes(self, obj):
        return obj.likes.count()

    def validate_content(self, value):
        if len(value) > MAX_BLOG_LENGTH:
            raise serializers.ValidationError("This blog is too long")
        return value



class BlogSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    parent = BlogCreateSerializer(read_only=True)
    class Meta:
        model = Blog
        fields = ['id', 'content', 'likes', 'is_repost', "parent"]

    def get_likes(self, obj):
        return obj.likes.count()

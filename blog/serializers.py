from blog.models import Post,Category
from rest_framework import serializers
from accounts.serializers import InstituteSerializer


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class PostDetailSerializer(serializers.ModelSerializer):
    author = InstituteSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Post
        fields = "__all__"


class PostEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "body", "category", "cover")
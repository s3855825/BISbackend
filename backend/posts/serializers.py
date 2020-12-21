from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.Serializer):
    class Meta:
        model = Post
        fields = {'title', 'message', 'author', }
        
    def create(self, validated_data):
        post = super().create(validated_data)
        post.save()
        return post
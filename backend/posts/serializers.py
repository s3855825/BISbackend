from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'message', 'author', 'group', )

    def create(self, validated_data):
        post = super().create(validated_data)
        post.save()
        return post

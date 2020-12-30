# from django.contrib.auth.models import User
from rest_framework import serializers

from .models import CustomUser, Review


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "password", "score",)
        read_only_fields = ("is_active",)
        # extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = super().create(validated_data)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(required=True, allow_blank=False)


class AccessTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.CharField()
    token = serializers.CharField()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('reviewee', 'review_message', 'review_score',)

    def create(self, validated_data):
        review = super().create(validated_data)
        review.save()
        return review

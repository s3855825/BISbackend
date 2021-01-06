from rest_framework import serializers

from .models import Notification


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "password", "friendcode", )
        read_only_fields = ("is_active",)
        # extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = super().create(validated_data)
        user.save()
        return user

class NotificationSerializer(serializers.Serializer):
    class Meta:
        model = Notification
        fields = ("notification_body", "receiver", )

    def create(self, validated_data):
        notification = super().create(validated_data)
        notification.save()
        return notification
        
from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.Serializer):
    class Meta:
        model = Notification
        fields = ("notification_body", "receiver", )

    def create(self, validated_data):
        notification = super().create(validated_data)
        notification.save()
        return notification
        
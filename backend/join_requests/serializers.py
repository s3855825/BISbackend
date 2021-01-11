from rest_framework import serializers

from .models import Request

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['title', 'sender_id', 'receiver_id', 'post_id', 'message', 'status', ]
    
    def create(self, validated_data):
        request = super().create(validated_data)
        request.save()
        return request

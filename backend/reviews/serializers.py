from rest_framework import serializers

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('reviewee', 'review_message', 'review_score',)

    def create(self, validated_data):
        review = super().create(validated_data)
        review.save()
        return review

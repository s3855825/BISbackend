from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string


# Create your models here.
class CustomUser(models.Model):
    class Meta:
        db_table = "User"

    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    score = models.FloatField(default=100.0)
    reviewed_times = models.IntegerField(default=0)


class Token(models.Model):
    class Meta:
        db_table = "Token"

    key = models.CharField(primary_key=True, max_length=255)
    user = models.ForeignKey(CustomUser, related_name='token', on_delete=models.CASCADE, to_field="id")
    created = models.DateTimeField(default=timezone.now)


class Review(models.Model):
    class Meta:
        db_table = "Review"

    reviewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reviewer", to_field="id")
    reviewee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reviewee", to_field="id")
    review_text = models.CharField(max_length=255)
    review_score = models.FloatField(default=0.0)
    review_time = models.DateTimeField(default=timezone.now)

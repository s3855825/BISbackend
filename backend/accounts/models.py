from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string


def generate_friend_code():
    char_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    return get_random_string(10, allowed_chars=char_list)

# Create your models here.
class CustomUser(models.Model):
    class Meta:
        db_table = "CustomUser"

    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    score = models.FloatField(default=100.0)
    reviewed_times = models.IntegerField(default=0)
    friendcode = models.CharField(max_length=10, default=generate_friend_code)


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

from django.db import models
from django.utils import timezone


# Create your models here.
class CustomUser(models.Model):
    class Meta:
        db_table = "User"

    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    # unique_code = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    point = models.FloatField(default=100.0)


class Token(models.Model):
    class Meta:
        db_table = "Token"

    key = models.CharField(primary_key=True, max_length=255)
    user = models.ForeignKey(CustomUser, related_name='token', on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)


class Review(models.Model):
    class Meta:
        db_table = "Review"

    reviewer = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    reviewee = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    review_text = models.CharField(max_length=255)
    review_score = models.FloatField(default=0.0)
    review_time = models.DateTimeField(default=timezone.now)

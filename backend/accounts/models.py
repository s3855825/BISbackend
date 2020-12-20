from django.db import models


# from django.contrib.auth.models import User

# Create your models here.
class CustomUser(models.Model):
    class Meta:
        db_table = "User"

    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)


class Token(models.Model):
    class Meta:
        db_table = "Token"

    key = models.CharField(primary_key=True, max_length=255)
    user = models.ForeignKey(CustomUser, related_name='token', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

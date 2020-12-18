from django.db import models

# Create your models here.
class Post(models.Model):
    class Meta:
        db_table = 'Post'

    title = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)

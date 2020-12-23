from django.db import models
from django.utils import timezone


# Create your models here.
class Post(models.Model):
    class Meta:
        db_table = 'Post'

    title = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)

    def __str__(self):
        return '{}: {}'.format(self.author.username, self.title)

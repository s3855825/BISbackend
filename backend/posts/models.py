from django.contrib.postgres.search import SearchVector, SearchVectorField
from django.contrib.postgres.indexes import GinIndex
from django.db import models
from django.utils import timezone


# Create your models here.
class Post(models.Model):
    class Meta:
        db_table = 'Post'
        indexes = [GinIndex(fields=['title_vector', 'message_vector']), ]

    title = models.CharField(max_length=255, blank=False, null=False)
    message = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)

    title_vector = SearchVectorField(null=True)
    message_vector = SearchVectorField(null=True)

    def __str__(self):
        return '{}: {}'.format(self.author.username, self.title)

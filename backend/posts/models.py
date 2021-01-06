from django.db import models
from django.utils import timezone


# Create your models here.
class PostManager(models.Manager):
    pass


class Post(models.Model):
    class Meta:
        db_table = 'Post'

    title = models.CharField(max_length=255, blank=False, null=False)
    message = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, to_field="id")
    group_id = models.IntegerField()

    # search_vector = SearchVectorField(null=True)
    objects = PostManager()

    def __str__(self):
        return '{}: {}'.format(self.author.username, self.title)

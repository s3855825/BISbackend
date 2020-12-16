from django.db import models

# Create your models here.
class Post(models.Model):
    class Meta:
        db_table = 'Post'

    id = models.IntegerField(primary_key=True, auto_created=True)
    title = models.CharField(max_length=255)
    message=models.CharField(max_length=255)
    
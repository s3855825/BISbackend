from django.db import models

# Create your models here.
class Request(models.Model):
    class Meta:
        db_table = "Request"

    title = models.CharField(max_length=255, blank=False, null=False)    
    sender = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name="receiver")
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    status = models.CharField(max_length=10)
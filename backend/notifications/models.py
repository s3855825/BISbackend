from django.db import models

# Create your models here.
class Notification(models.Model):
    class Meta:
        db_table = "Notification"

    notification_body = models.CharField(max_length=255)
    receiver = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, to_field="id")

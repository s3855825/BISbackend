from django.db import models

# Create your models here.
class Group(models.Model):
    class Meta:
        db_table = "Group"
    
    id = models.AutoField(primary_key=True, auto_created=True)
    group_name = models.CharField(max_length=255)


class GroupMember(models.Model):
    class Meta:
        db_table = "Member"

    id = models.AutoField(primary_key=True, auto_created=True)
    group_id = models.ForeignKey('Group', on_delete=models.CASCADE)
    member_id = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)

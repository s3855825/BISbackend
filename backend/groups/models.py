from django.db import models

# Create your models here.
class Group(models.Model):
    class Meta:
        db_table = "Group"
    
    group_name = models.CharField(max_length=255)


class GroupMember(models.Model):
    class Meta:
        db_table = "Member"

    group_id = models.ForeignKey('Group.id', on_delete=models.CASCADE)
    member_id = models.ForeignKey('accounts.CustomUser.id', on_delete=models.CASCADE)

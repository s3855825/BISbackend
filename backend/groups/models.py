from django.db import models
from django.utils import timezone


# Create your models here.
class Group(models.Model):
    class Meta:
        db_table = "Group"

    group_name = models.CharField(max_length=255)


class GroupMember(models.Model):
    class Meta:
        db_table = "GroupMember"

    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    member_id = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)


class Task(models.Model):
    class Meta:
        db_table = "Task"

    task_name = models.CharField(max_length=40)
    task_description = models.CharField(max_length=255, blank=True)
    author = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    created_time = models.DateTimeField(default=timezone.now)
    deadline = models.DateTimeField(default=None)


class GroupTask(models.Model):
    class Meta:
        db_table = "GroupTask"

    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)


class TaskMember(models.Model):
    class Meta:
        db_table = "TaskMember"

    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    member_id = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)

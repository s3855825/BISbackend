from rest_framework import serializers

from .models import Group, GroupMember, Task, TaskMember, GroupTask


class GroupSerializer(serializers.Serializer):
    class Meta:
        model = Group
        fields = {"group name", }


class GroupMemberSerializer(serializers.Serializer):
    class Meta:
        model = GroupMember
        fields = {"group_id", "member_id", }


class TaskSerializer(serializers.Serializer):
    class Meta:
        model = Task
        fields = {"task_name", "description", "created_time", "deadline", "tags", }


class GroupTaskSerializer(serializers.Serializer):
    class Meta:
        model = GroupTask
        fields = {"group_id", "task_id", }


class TaskMemberSerializer(serializers.Serializer):
    class Meta:
        model = TaskMember
        fields = {"task_id", "member_id", }

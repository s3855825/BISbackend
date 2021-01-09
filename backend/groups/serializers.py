from rest_framework import serializers

from .models import Group, GroupMember, Task, TaskMember, GroupTask


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "group_name",)

    def create(self, validated_data):
        group = super().create(validated_data)
        group.save()
        return group


class GroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMember
        fields = ("group_id", "member_id",)


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("task_name", "task_description", "created_time", "deadline",)


class GroupTaskSerializer(serializers.Serializer):
    class Meta:
        model = GroupTask
        fields = ("group_id", "task_id",)


class TaskMemberSerializer(serializers.Serializer):
    class Meta:
        model = TaskMember
        fields = ("task_id", "member_id",)

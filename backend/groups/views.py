# Create your views here.
import json
import rest_framework.status as status
from django.contrib.auth.models import AnonymousUser
from django.http import Http404
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Group, Task, GroupMember, GroupTask
from .serializers import GroupSerializer, TaskSerializer, GroupMemberSerializer, GroupTaskSerializer
from accounts.models import CustomUser
from accounts.serializers import UserSerializer


class HTTP401(AuthenticationFailed):
    pass


class GroupView(APIView):
    def get(self, request, format=None):
        """
        show all groups
        """
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        if not serializer.data:
            return Response({'EmptyGroupList': 'No group created!'})
        return serializer.data

    def post(self, request, format=None):
        """
        create new groups
        """
        group_serializer = GroupSerializer(data=request.data)
        if group_serializer.is_valid(raise_exception=True):
            group_serializer.save()
            return Response(data=group_serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=group_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupDetailView(APIView):
    def get(self, request, primary_key, format=None):
        """
        show group details
        """
        try:
            group = Group.objects.filter(pk=primary_key)
            serializer = GroupSerializer(group)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Group.DoesNotExist:
            raise Http404('Group does not exist')

    def put(self, request, primary_key, format=None):
        """
        modify group details
        """
        try:
            group = Group.objects.get(pk=primary_key)
            serializer = GroupSerializer(group, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Group.DoesNotExist:
            raise Http404('Group does not exist')

    def delete(self, request, primary_key, format=None):
        """
        delete group
        """
        try:
            group = Group.objects.get(pk=primary_key)
            group.delete()
            return Response(data=[], status=status.HTTP_200_OK)
        except Group.DoesNotExist:
            raise Http404('Group does not exist')


class GroupMemberView(APIView):
    def get(self, request, primary_key, format=None):
        """
        show all members in group
        """
        # get group
        group = Group.objects.filter(pk=primary_key)
        if not group:
            raise Http404('Group does not exist')
        member_queryset = GroupMember.objects.filter(group_id=group.id)
        response_data = []
        if member.count <= 0:
            return Response({'EmptyUserList': 'No account in group yet'}, status=status.HTTP_200_OK)
        else:
            for member in member_queryset:
                serializer = UserSerializer(data=member.data)
                response_data.append(serializer.data)
            response_data = json.dumps(response_data)
            return Response(data=response_data, status=status.HTTP_200_OK)


    def post(self, request, primary_key, format=None):
        """
        add member to group
        """
        group = Group.objects.filter(pk=primary_key)
        if not group:
            raise Http404('Group does not exist')
        serializer_data = {'group_id': group.id, 'member_id': request.data['user_id']}
        serializer = GroupMemberSerializer(data=serializer_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data={}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def delete(self, request, primary_key, format=None):
        """
        delete member from group
        """
        group = Group.objects.filter(pk=primary_key)
        if not group:
            raise Http404('Group does not exist')
        user_id = request.data['user_id']
        memberlist_queryset = GroupMember.objects.filter(group_id=group.id, member_id=user_id)
        if memberlist_queryset.count == 0:
            return Http404('No user in group')
        else:
            memberlist_queryset.delete()
            return Response(data={'': 'User removed from group'}, status=status.HTTP_200_OK)


class GroupTaskView(APIView):
    def get(self, request, format=None):
        """
        show all tasks in group
        """
        group = Group.objects.filter(pk=primary_key)
        if not group:
            raise Http404('Group does not exist')
        task_queryset = GroupTask.objects.filter(group_id=group.id)
        response_data = []
        if task_queryset.count <= 0:
            return Response({'EmptyTaskList': 'No task in group yet'}, status=status.HTTP_200_OK)
        else:
            for task in task_queryset:
                serializer = TaskSerializer(data=task.data)
                response_data.append(serializer.data)
            response_data = json.dumps(response_data)
            return Response(data=response_data, status=status.HTTP_200_OK)

    def post(self, request, primary_key, format=None):
        """
        add task to group
        """
        group = Group.objects.filter(pk=primary_key)
        if not group:
            raise Http404('Group does not exist')

        task_serializer_data = {'task_name': request.data['task_name'],
                                'description': request.data['task_description'],
                                }
        task_serializer = TaskSerializer(data=task_serializer_data)

        if task_serializer.is_valid(raise_exception=True):
            task_serializer.save()
            group_task_serializer = GroupTaskSerializer(data={'group_id': group.id, })
            return Response(data={}, status=status.HTTP_200_OK)

        return Response(task_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, primary_key, format=None):
        """
        edit task in group or add member to task
        """
        group = Group.objects.filter(pk=primary_key)
        if not group:
            raise Http404('Group does not exist')
        task = Task.objects.filter(pk=request.data['task_id'])
        if not group:
            raise Http404('Task does not exist')
        serializer_data = {'group_id': group.id, 'task_id': request.data['task_id']}
        serializer = GroupMemberSerializer(data=serializer_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data={}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, primary_key, format=None):
        """
        delete task in group
        """
        group = Group.objects.filter(pk=primary_key)
        if not group:
            raise Http404('Group does not exist')
        task_id = request.data['task_id']
        tasklist_queryset = GroupTask.objects.filter(group_id=group.id, task_id=task_id)
        if tasklist_queryset.count == 0:
            return Http404('No task in group')
        else:
            tasklist_queryset.delete()
            return Response(data={'': 'Task removed from group'}, status=status.HTTP_200_OK)

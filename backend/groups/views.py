# Create your views here.

import rest_framework.status as status
from accounts.models import CustomUser
from django.http import Http404
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Group, Task, GroupMember, GroupTask
from .serializers import GroupSerializer, GroupMemberSerializer, GroupTaskSerializer, TaskSerializer


class HTTP401(AuthenticationFailed):
    pass


class GroupView(APIView):
    def get(self, request, format=None):
        """
        show all groups
        """
        group_queryset = Group.objects.all()
        serializer = GroupSerializer(group_queryset, many=True)
        if not serializer.data:
            return Response({'EmptyGroupList': 'No group created!'})
        response_data = []
        for group in group_queryset:
            data = {
                'id': group.id,
                'name': group.group_name,
            }
            response_data.append(data)
        return Response(data=response_data)

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
            group_queryset = Group.objects.get(pk=primary_key)
            serializer = GroupSerializer(group_queryset)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Group.DoesNotExist:
            raise Http404('This group does not exist')

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
        group = Group.objects.get(pk=primary_key)
        if not group:
            raise Http404('Group does not exist')
        member_queryset = GroupMember.objects.filter(group_id=group.id)

        response_data = []
        if len(member_queryset) <= 0:
            return Response({'EmptyUserList': 'No account in group yet'}, status=status.HTTP_200_OK)
        else:
            for member in member_queryset:
                user = CustomUser.objects.get(pk=member.member_id.id)
                data = {
                    'member_id': user.id,
                    'member_name': user.username,
                }
                response_data.append(data)
            return Response(data=response_data, status=status.HTTP_200_OK)

    def post(self, request, primary_key, format=None):
        """
        add member to group
        """
        group = Group.objects.get(pk=primary_key)
        if not group:
            raise Http404('Group does not exist')

        group_member_queryset = GroupMember.objects.filter(group_id=group.id, member_id=request.data['user_id'])
        if len(group_member_queryset) >= 1:
            return Response(data={'UserAlreadyExist': 'This user is already in this group'},
                            status=status.HTTP_200_OK)

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
        group = Group.objects.get(pk=primary_key)
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
    def get(self, request, primary_key, format=None):
        """
        show all tasks in group
        """
        group = Group.objects.get(pk=primary_key)
        if not group:
            raise Http404('Group does not exist')
        task_queryset = GroupTask.objects.filter(group_id=group.id)
        response_data = []
        if len(task_queryset) <= 0:
            return Response({'EmptyTaskList': 'No task in group yet'}, status=status.HTTP_200_OK)
        else:
            for listed_task in task_queryset:
                task = Task.objects.get(pk=listed_task.id.id)
                data = {
                    'task_id': task.id,
                    'task_name': task.task_name,
                    'task_author_name': task.author.username,
                    'task_create_date': task.created_time,
                    'task_deadline': task.deadline,
                }
                response_data.append(data)
            return Response(data=response_data, status=status.HTTP_200_OK)

    def post(self, request, primary_key, format=None):
        """
        add task to group
        """
        group = Group.objects.get(pk=primary_key)
        if not group:
            raise Http404('Group does not exist')

        task_data = {
            'task_name': request.data['task_name'],
            'task_description': request.data['task_description'],
            'author': request.data['author']
        }
        task_serializer = TaskSerializer(data=task_data)
        if task_serializer.is_valid(raise_exception=True):
            task = task_serializer.save()

        gt_serializer_data = {'group_id': group.id, 'task_id': task.id}
        gt_serializer = GroupTaskSerializer(data=gt_serializer_data)
        if gt_serializer.is_valid(raise_exception=True):
            gt_serializer.save()
            return Response(data=gt_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(gt_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, primary_key, format=None):
        """
        modify task's details
        """
        group = Group.objects.get(pk=primary_key)
        if not group:
            raise Http404('Group does not exist')
        
        group_task_queryset = GroupTask.objects.filter(group_id=group.id)
        if len(group_task_queryset) == 0:
            return Http404('Task does not exist in group')


        serializer_data = {'group_id': group.id, 'name': request.data['task_name']}
        serializer = GroupTaskSerializer(data=serializer_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data={}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, primary_key, format=None):
        """
        delete task in group
        """
        group = Group.objects.get(pk=primary_key)
        if not group:
            raise Http404('Group does not exist')
        task_id = request.data['task_id']
        tasklist_queryset = GroupTask.objects.filter(group_id=group.id, task_id=task_id)
        if tasklist_queryset.count == 0:
            return Http404('No such task in group')
        else:
            tasklist_queryset.delete()
            return Response(data={'': 'Task removed from group'}, status=status.HTTP_200_OK)

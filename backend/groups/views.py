# Create your views here.
import rest_framework.status as status
from django.contrib.auth.models import AnonymousUser
from django.http import Http404
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Group, Task
from .serializers import GroupSerializer, TaskSerializer


class HTTP401(AuthenticationFailed):
    pass


class GroupView(APIView):
    def get(self, request, format=None):
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        if not serializer.data:
            return Response({'EmptyGroupList': 'No group created!'})
        return serializer.data

    def post(self, request, format=None):
        group_serializer = GroupSerializer(data=request.data)
        if group_serializer.is_valid(raise_exception=True):
            group_serializer.save()
            return Response(data=group_serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=group_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupDetailView(APIView):
    def get(self, request, primary_key, format=None):
        try:
            group = Group.objects.filter(pk=primary_key)
            serializer = GroupSerializer(group)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Group.DoesNotExist:
            raise HTTP401

    def put(self, request, primary_key, format=None):
        try:
            group = Group.objects.get(pk=primary_key)
            serializer = GroupSerializer(group, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Group.DoesNotExist:
            raise Http404

    def delete(self, request, primary_key, format=None):
        try:
            group = Group.objects.get(pk=primary_key)
            group.delete()
            return Response(data=[], status=status.HTTP_200_OK)
        except Group.DoesNotExist:
            raise Http404


class TaskView(APIView):
    def get(self, request, primary_key, format=None):
        """
        Get all tasks belonging to a group.
        """
        if isinstance(request.user, AnonymousUser):
            return Response(data={'Unauthorized': 'User must log in to view content'},
                            status=status.HTTP_401_UNAUTHORIZED)
        task = Task.objects.filter(author=request.user)
        task_serializer = TaskSerializer(data=task, many=True)
        if not task_serializer:
            return Response(data={'EmptyTaskList': 'No task in this group yet :<'}, status=status.HTTP_200_OK)
        return Response(data=task_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, primary_key, format=None):
        pass


class TaskDetailView(APIView):
    pass

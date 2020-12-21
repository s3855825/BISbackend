import json
import rest_framework.status as status
from django.http import Http404
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post
from .serializers import PostSerializer


class HTTP401(AuthenticationFailed):
    pass


# Create your views here.
class PostView(APIView):    
    def get(self, request, format=None):
        post_queryset = Post.objects.all()
        serializer = PostSerializer(post_queryset, many=True)
        if not serializer.data:
            return Response({'EmptyPostList': 'No post made!'})
        response_data = []
        for post in post_queryset:
            data = {
                'id': post.id,
                'title': post.title,
                'message': post.message,
                'author_id': post.author.id,
            }
            response_data.append(data)
            response_data = json.dumps(response_data)
        return Response(data=response_data)

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    def get(self, request, primary_key, format=None):
        try:
            print('PRIMARY KEY: ', primary_key)
            post_queryset = Post.objects.filter(pk=primary_key)
            if post_queryset.count > 0:
                serializer = PostSerializer(post_queryset[0])
                return Response(data=serializer.data, status=status.HTTP_200_OK)
        except IndexError:
            raise Http404('Post does not exist')

    def put(self, request, primary_key, format=None):
        try:
            post_queryset = Post.objects.get(pk=primary_key)
            if post_queryset.count > 0:
                post = post_queryset[0]
                serializer = PostSerializer(post, data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            raise Http404('Post does not exist')

    def delete(self, request, primary_key, format=None):
        try:
            post = Post.objects.get(pk=primary_key)
            post.delete()
            return Response(data=[], status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            raise Http404

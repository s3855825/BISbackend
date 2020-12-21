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
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        if not serializer.data:
            return Response({'EmptyPostList': 'No post made!'})
        return Response(serializer.data)

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
            post = Post.objects.filter(id=primary_key)
            serializer = PostSerializer(post)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            raise Http404

    def put(self, request, primary_key, format=None):
        try:
            post = Post.objects.get(pk=primary_key)
            serializer = PostSerializer(post, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            raise Http404

    def delete(self, request, primary_key, format=None):
        try:
            post = Post.objects.get(pk=primary_key)
            post.delete()
            return Response(data=[], status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            raise Http404

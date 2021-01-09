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
                'author_name': post.author.username,
                'group_id': post.group,
            }
            response_data.append(data)
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
            post_queryset = Post.objects.get(pk=primary_key)
            serializer = PostSerializer(post_queryset[0])
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
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


class PostSearchView(APIView):
    def post(self, request, format=None):
        query_text = request.data['querytext']
        if not query_text:
            return Response({'': "Empty search phrase"}, status=status.HTTP_400_BAD_REQUEST)

        title_search_result = Post.objects.filter(title__search=query_text)
        message_search_result = Post.objects.filter(message__search=query_text)

        print(title_search_result)
        print(message_search_result)

        response_data = []
        for post in title_search_result:
            data = {
                'id': post.id,
                'title': post.title,
                'message': post.message,
                'author_id': post.author.id,
                'author_name': post.author.username,
            }
            print(data)
            response_data.append(data)

        for post in message_search_result:
            data = {
                'id': post.id,
                'title': post.title,
                'message': post.message,
                'author_id': post.author.id,
            }
            print(data)
            response_data.append(data)

        return Response(data=response_data, status=status.HTTP_200_OK)

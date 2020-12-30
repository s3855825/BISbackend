import binascii
import os

from django.http import Http404
from posts.models import Post
from groups.models import GroupMember
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser, Token, Review
from .serializers import LoginSerializer, UserSerializer, AccessTokenSerializer, ReviewSerializer


def generate_token(user_id):
    token_string = binascii.hexlify(os.urandom(32)).decode()
    # access_token = {user_id: token_string}
    access_token = '{}: {}'.format(user_id, token_string)
    return access_token


class HTTP401(AuthenticationFailed):
    pass


# Create your views here.
class UserView(APIView):
    serializer_class = UserSerializer
    model = CustomUser

    def get(self, request, format=None):
        # return the list of all users
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        if not serializer.data:
            return Response({'EmptyUserList': 'No user registered'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            if CustomUser.objects.filter(username=username).exists() or CustomUser.objects.filter(email=email).exists():
                raise HTTP401("This username or email is already in used.")
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    def get(self, request, primary_key, format=None):
        try:
            user_queryset = CustomUser.objects.filter(pk=primary_key)
            if len(user_queryset) > 0:
                user = user_queryset[0]
                serializer = UserSerializer(user)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(data={'ErrorMessage': 'No user found'}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            raise Http404

    def put(self, request, primary_key, format=None):
        try:
            user_queryset = CustomUser.objects.get(pk=primary_key)
            if user_queryset.count > 0:
                user = user_queryset[0]
                serializer = UserSerializer(user, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_200_OK)
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data={'ErrorMessage': 'No user found'}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            raise Http404

    def delete(self, request, primary_key, format=None):
        try:
            user = CustomUser.objects.get(pk=primary_key)
            user.delete()
            return Response(data=[], status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            raise Http404


class UserAuthView(APIView):
    def post(self, request, format=None):
        login_serializer = LoginSerializer(data=request.data)
        if login_serializer.is_valid(raise_exception=True):
            serialized_username = login_serializer.data['username']
            serialized_password = login_serializer.data['password']

            queryset = CustomUser.objects.filter(username=serialized_username)
            user = None
            if len(queryset) > 0:
                for queried_user in queryset:
                    if (queried_user.password == serialized_password):
                        user = queried_user

            if not user:
                raise HTTP401('Incorrect username or password.')

            token_string = generate_token(user.id)
            token = Token.objects.create(key=token_string, user=user)
            data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'token': token.key,
            }
            token_serializer = AccessTokenSerializer(data=data)
            if token_serializer.is_valid():
                return Response(data=token_serializer.data, status=status.HTTP_200_OK)
            else:
                raise HTTP401(token_serializer.errors)


class UserPostView(APIView):
    def get(self, request, primary_key, format=None):
        # current_user = CustomUser.objects.get(primary_key)
        user_post_queryset = Post.objects.filter(author=primary_key)
        if len(user_post_queryset) == 0:
            return Response(data={'': "You don't have any post yet :<"}, status=status.HTTP_200_OK)
        response_data = []
        for post in user_post_queryset:
            data = {
                'id': post.id,
                'title': post.title,
                'message': post.message,
                'author_id': post.author.id,
                'author_name': post.author.username,
                'created_time': post.timestamp,
            }
            response_data.append(data)
        return Response(data=response_data, status=status.HTTP_200_OK)



class UserGroupView(APIView):
    def get(self, request, primary_key, format=None):
        user_group_queryset = GroupMember.objects.filter(author=primary_key)
        if len(user_group_queryset) == 0:
            return Response(data={'': "You don't have any group yet :<"}, status=status.HTTP_200_OK)
        response_data = []
        for member_group in user_group_queryset:
            data = {
                'id': member_group.group_id.id,
                'group_name': member_group.group_id.title,
             }
            response_data.append(data)
        return Response(data=response_data, status=status.HTTP_200_OK)


class UserReviewView(APIView):
    def get(self, request, primary_key, format=None):
        """
        Get all reviews given by a user
        """
        review_queryset = Review.objects.filter(reviewer=primary_key)
        if len(review_queryset) == 0:
            return Response(data={'': "You don't have any review yet"}, status=status.HTTP_200_OK)
        response_data = []
        for review in review_queryset:
            data = {
                'id': review.id,
                'reviee': review.reviewee,
                'message': review.review_message,
                'score': review.review_score,
            }
            response_data.append(data)
        return Response(data=response_data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        """
        Create a new review
        """
        review_serializer = ReviewSerializer(data=request.data)
        if review_serializer.is_valid(raise_exception=True):
            review_serializer.save()
            return Response(data=review_serializer.data, status=status.HTTP_201_CREATED)
        return Response(review_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

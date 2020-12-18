import binascii
import os

from django.contrib.auth import authenticate
# from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, UserSerializer, AccessTokenSerializer
from .models import CustomUser, Token


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
            return Response({'EmptyUserList': 'No user registered'})
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
            user = CustomUser.objects.get(pk=primary_key)
            serializer = UserSerializer(user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            raise Http404

    def put(self, request, primary_key, format=None):
        try:
            user = CustomUser.objects.get(pk=primary_key)
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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

            # user = authenticate(username=serialized_username,
            #                     password=serialized_password)

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

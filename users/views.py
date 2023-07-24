from rest_framework.response import Response
from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from django.contrib.auth import authenticate, login, logout
from . import serializers
from .models import User


# class Me(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         serializer = serializers.PrivateUserSerializer(user)
#         return Response(serializer.data)

#     def put(self, request):
#         user = request.user
#         serializer = serializers.PrivateUserSerializer(
#             user, data=request.data, partial=True
#         )
#         if serializer.is_valid():
#             update_data = serializer.save()
#             return Response(serializers.PrivateUserSerializer(update_data).data)
#         else:
#             return Response(serializer.errors)


class Me(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = serializers.PrivateUserSerializer

    def get(self, request, *args, **kwargs):
        queryset = request.user
        return Response(serializers.PrivateUserSerializer(queryset).data)

    def put(self, request, *args, **kwargs):
        queryset = request.user
        serializer = serializers.PrivateUserSerializer(
            queryset,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class Users(generics.GenericAPIView):
    serializer_class = serializers.PrivateUserSerializer

    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise ParseError
        serializer = serializers.PrivateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class PublicUser(generics.GenericAPIView):
    serializer_class = serializers.PrivateUserSerializer

    def get(self, request, username):
        user = User.objects.get(username=username)
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise ParseError
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            login(request, user)
            return Response({"ok": "접속 되었습니다."})
        else:
            return Response({"error": "아이디 혹은 비밀번호가 잘못 되었습니다."})


class LogOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"Bye": "접속을 종료하셨습니다."})

from rest_framework.response import Response
from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
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


class ChangePassword(generics.GenericAPIView):
    serializer_class = serializers.PrivateUserSerializer

    def put(self, request):
        pass

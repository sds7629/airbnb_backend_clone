from rest_framework.response import Response
from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ParseError
from . import serializers
from categories.models import Category
from .models import Experience


class Experiences(
    generics.ListCreateAPIView,
):
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Experience.objects.all()
    serializer_class = serializers.ListExperienceSerializer

    def create(self, request, *args, **kwargs):
        category_pk = request.data.get("category")
        category = Category.objects.get(pk=category_pk)
        if category != Category.CategoryKindChoices.EXPERIENCES:
            raise ParseError("액티비티만 올릴 수 있습니다!")
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(
                category=category,
                host=request.user,
            )
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

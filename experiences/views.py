from rest_framework.response import Response
from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ParseError, NotFound, PermissionDenied
from django.utils import timezone
from . import serializers
from bookings.serializer import (
    CreateExperienceBookingSerializer,
    PublicBookingSerializer,
    DetailBookingSerializer,
)
from bookings.models import Booking
from categories.models import Category
from .models import Experience, Perk


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
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ExperiencesDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Experience.objects.all()
    serializer_class = serializers.DetailExperienceSerializer

    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        if Experience.objects.get(pk=pk).category.kind != Category.CategoryKindChoices.EXPERIENCES:
            raise ParseError("액티비티 카테고리가 아닙니다!")
        else:
            return self.retrieve(request)

    def put(self, request, *args, **kwargs):
        return self.update(request)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request)


class ExperiencePerk(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Experience.objects.all()
    serializer_class = serializers.PerkExperienceSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request)


class ExperienceBooking(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = PublicBookingSerializer

    def get_experience(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except:
            raise NotFound

    def get_queryset(self):
        experience = self.get_experience(self.kwargs["pk"])
        now = timezone.localtime(timezone.now())
        return Booking.objects.filter(
            experience=experience,
            kind=Booking.BookingKindChoices.EXPERIENCE,
            experience_time__gte=now,
        )

    def create(self, request, *args, **kwargs):
        experience = self.get_experience(self.kwargs["pk"])
        serializer = CreateExperienceBookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            experience=experience,
            user=request.user,
            kind=Booking.BookingKindChoices.EXPERIENCE,
        )
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get(self, request, *args, **kwargs):
        return self.list(request)

    def post(self, request, *args, **kwargs):
        return self.create(request)


class ExperienceDetailBooking(
    generics.ListAPIView,
    generics.UpdateAPIView,
    generics.DestroyAPIView,
):
    permission_classes = [IsAuthenticated]

    serializer_class = DetailBookingSerializer

    def get_experience(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except:
            raise NotFound

    def get_queryset(self):
        experience = self.get_experience(self.kwargs["pk"])
        now = timezone.localtime(timezone.now())
        return Booking.objects.filter(
            pk=self.kwargs["booking_pk"],
            experience=experience,
            kind=Booking.BookingKindChoices.EXPERIENCE,
            experience_time__gte=now,
        )

    def get(self, request, *args, **kwargs):
        return self.list(request)

    def put(self, request, *args, **kwargs):
        return self.update(request)

    def delete(self, request, *args, **kwargs):
        instance = self.get_queryset()

        if instance[0].user != request.user:
            raise PermissionDenied
        else:
            instance[0].delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class Perks(
    generics.ListCreateAPIView,
):
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Perk.objects.all()
    serializer_class = serializers.PerkSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PerkDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Perk.objects.all()
    serializer_class = serializers.PerkExperienceSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request)

from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import mixins, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from .serializer import (
    RoomListSerializer,
    RoomDetailSerializer,
    AmenitySerializer,
    AmenityDetailSerializer,
)
from rest_framework.views import APIView
from rest_framework.exceptions import (
    NotFound,
    ParseError,
    NotAuthenticated,
    PermissionDenied,
)
from .models import Room, Amenity
from categories.models import Category
from reviews.serializers import ReviewSerializer
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from medias.models import Photo
from medias.serializer import PhotoSerializer
from bookings.models import Booking
from bookings.serializer import PublicBookingSerializer, CreateRoomBookingSerializer


class Amenity(APIView):
    def get(self, request):
        all_Amenity = Amenity.objects.all()
        serializer = AmenitySerializer(all_Amenity)
        return Response(serializer.data)

    def post(self, request):
        amenity_upload = AmenitySerializer(data=request.data)
        if amenity_upload.is_valid():
            amenity = amenity_upload.save()
            serializer = AmenitySerializer(amenity)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            return NotFound

    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenityDetailSerializer(amenity)
        return Response(serializer.data)

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenityDetailSerializer(
            amenity,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            update_amenity = serializer.save()
            return Response(AmenityDetailSerializer(update_amenity).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Rooms(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(all_rooms, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RoomDetailSerializer(data=request.data)
        if request.user.is_authenticated:
            if serializer.is_valid():
                category_pk = request.data.get("category")
                if not category_pk:
                    raise ParseError("Category is required.")
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The category kind should be 'rooms'")
                except Category.DoesNotExist:
                    raise ParseError("Category Not Found")
                room = serializer.save(
                    owner=request.user,
                    category=category,
                )
                amenities = request.data.get("amenities")
                for amenity_pk in amenities:
                    try:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                    except Amenity.DoesNotExist:
                        room.delete()
                        raise ParseError(f"Amenity with id{amenity_pk} not found")
                    room.amenities.add(amenity)  # ManyToMany의 관계일 때 사욯가능
                serializer = RoomDetailSerializer(room)
                return Response(serializer.data)
            else:
                return Response(serializer.errors)


class RoomDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_objects(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_objects(pk)
        serializer = RoomDetailSerializer(
            room,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        room = self.get_objects(pk)
        serializer = RoomDetailSerializer(
            room,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            category_pk = request.data.get("category")
            amenities = request.data.get("amenities")
            category = Category.objects.get(pk=category_pk)

            room_update = serializer.save(
                owner=request.user,
                category=category,
            )
            for amenity_pk in amenities:
                amenity = Amenity.objects.get(pk=amenity_pk)
                room_update.amenities.add(amenity)

            serializer = RoomDetailSerializer(room_update)
            return Response(serializer.data)

    def delete(self, request, pk):
        room = self.get_objects(pk)
        if room.owner != request.user:
            raise PermissionDenied

        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class RoomReviews(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.GET.get("page", 1)
            print(page)
            page = int(page)
        except ValueError:
            page = settings.PAGE_SIZE
        page_size = 3
        start = (page - 1) * page_size
        end = start + page_size
        room = self.get_object(pk)
        serializer = ReviewSerializer(
            room.reviews.all()[start:end],
            many=True,
        )
        return Response(serializer.data)

    def post(selt, request, pk):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(
                user=request.user,
                room=self.get_object(pk),
            )
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class RoomPhotos(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        room = self.get_object(pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if request.user != room.owner:
            raise PermissionError
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(room=room)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class RoomBookings(
    mixins.ListModelMixin,
    generics.GenericAPIView,
):
    serializer_class = PublicBookingSerializer

    def get_room(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except:
            raise NotFound

    def get_queryset(self):
        room = self.get_room(self.kwargs["pk"])
        now = timezone.localtime(timezone.now()).date()
        return Booking.objects.filter(
            room=room,
            kind=Booking.BookingKindChoices.ROOM,
            check_in__gt=now,
        )

    def get(self, request, *args, **kwargs):
        return self.list(request)

    def post(self, request, *args, **kwargs):
        room = self.get_room(kwargs["pk"])
        serializer = CreateRoomBookingSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save(
                room=room,
                user=request.user,
                kind=Booking.BookingKindChoices.ROOM,
            )
            serializer = PublicBookingSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

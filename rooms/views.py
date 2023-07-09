from django.shortcuts import render
from rest_framework.response import Response
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
from rest_framework.status import HTTP_204_NO_CONTENT


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


class Rooms(APIView):
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
    def get_objects(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_objects(pk)
        serializer = RoomDetailSerializer(room)
        return Response(serializer.data)

    def put(self, request, pk):
        room = self.get_objects(pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if room.owner != request.user:
            raise PermissionDenied
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
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if room.owner != request.user:
            raise PermissionDenied

        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    # def get(self, request, pk):
    #     pass

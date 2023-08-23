from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK
from .models import Wishlist
from rooms.models import Room
from .serializer import WishlistSerializer


class WishLists(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlists = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(wishlists, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WishlistSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.save(user=request.user)
            serializer = WishlistSerializer(name)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WishListDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_list(self, pk):
        try:
            return Wishlist.objects.get(pk=pk)
        except Wishlist.DoesNotExist:
            raise NotFound

    def get_room(self, room_pk):
        try:
            return Room.objects.get(pk=room_pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        wishlist = self.get_list(pk)
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)

    def put(self, request, pk):
        wishlist = self.get_list(pk)
        serializer = WishlistSerializer(
            wishlist,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            save_wishlist = serializer.save()
            serializer = WishlistSerializer(save_wishlist)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WishlistToggle(APIView):
    permission_classes = [IsAuthenticated]

    def get_list(self, pk, user):
        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise NotFound

    def get_room(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def put(self, request, pk, room_pk):
        wishlist = self.get_list(pk, request.user)
        room = self.get_room(room_pk)

        if wishlist.rooms.filter(pk=room.pk).exists():
            wishlist.rooms.remove(room)
        else:
            wishlist.rooms.add(room)
        return Response(status=HTTP_200_OK)

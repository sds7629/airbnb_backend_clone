from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Wishlist
from .serializer import WishlistSerializer


class WishLists(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wisilists = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(wisilists, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WishlistSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.save(user=request.user)
            serializer = WishlistSerializer(name)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

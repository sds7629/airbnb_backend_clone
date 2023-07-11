from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Photo
from rest_framework.exceptions import NotFound, PermissionDenied

# Create your views here.


class PhotoDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_objects(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise NotFound

    def delete(self, request, pk):
        photo = self.get_objects(pk)
        if (photo.room and photo.room.owner != request.user) or (
            photo.experiences and photo.experiences.host != request.user
        ):
            raise PermissionDenied
        photo.delete()
        return Response(status=HTTP_204_NO_CONTENT)

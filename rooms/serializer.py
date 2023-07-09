from rest_framework import serializers
from .models import Room, Amenity
from categories.serializer import CategorySerializer
from medias.serializer import PhotoSerializer
from users.serializer import TinyUserSerializer
from reviews.models import Review


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )


class AmenityDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = "__all__"


class RoomDetailSerializer(serializers.ModelSerializer):
    owner = TinyUserSerializer(read_only=True)
    amenities = AmenitySerializer(
        read_only=True,
        many=True,
    )
    category = CategorySerializer(
        read_only=True,
    )
    rating = serializers.SerializerMethodField()
    # is_owner = serializers.SerializerMethodField()
    # photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = "__all__"

    def get_rating(self, room):
        return room.rating()

    # def get_is_owner(self, room):
    #     request = self.context["request"]
    #     return room.owner == request.user


class RoomListSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
        )

    def get_rating(self, room):
        return room.rating()

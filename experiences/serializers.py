from rest_framework.serializers import ModelSerializer
from .models import Experience, Perk
from categories.serializer import CategorySerializer


class ListExperienceSerializer(ModelSerializer):
    class Meta:
        model = Experience
        fields = (
            "country",
            "city",
            "name",
            "price",
            "start",
            "end",
            "category",
        )


class PerkSerializer(ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"


class DetailExperienceSerializer(ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Experience
        fields = "__all__"


class PerkExperienceSerializer(ModelSerializer):
    perks = PerkSerializer(read_only=True, many=True)

    class Meta:
        model = Experience
        fields = ("perks",)

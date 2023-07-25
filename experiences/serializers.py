from rest_framework.serializers import ModelSerializer
from .models import Experience


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

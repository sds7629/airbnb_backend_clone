from rest_framework import serializers
from users.serializers import TinyUserSerializer
from .models import Booking
from django.utils import timezone


class CreateExperienceBookingSerializer(serializers.ModelSerializer):
    experience_time = serializers.DateTimeField()

    def validate_experience_time(self, value):
        now_date = timezone.localtime(timezone.now()).date()
        now_time = timezone.localtime(timezone.now()).time()
        if now_date > value.date():
            raise serializers.ValidationError("지나간 날짜는 예약할 수 없어요!")
        if now_time > value.time():
            raise serializers.ValidationError("지나간 시간은 예약 할 수 없어요!")
        else:
            return value

    class Meta:
        model = Booking
        fields = (
            "experience_time",
            "guest",
        )


class CreateRoomBookingSerializer(serializers.ModelSerializer):
    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guest",
        )

    def validate_check_in(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("지나간 날짜는 예약할 수 없어요!")

        return value

    def validate_check_out(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("지나간 날짜는 예약할 수 없어요!")

        return value

    def validate(self, data):
        if data["check_out"] <= data["check_in"]:
            raise serializers.ValidationError("체크 아웃 날짜는 체크 인 날짜를 넘을 수 없습니다!")

        if Booking.objects.filter(
            check_in__lte=data["check_out"],
            check_out__gte=data["check_in"],
        ).exists():
            raise serializers.ValidationError("이미 예약이 되어 있습니다.")
        return data


class PublicBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "experience_time",
            "guest",
            "user",
        )


class DetailBookingSerializer(serializers.ModelSerializer):
    user = TinyUserSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = "__all__"

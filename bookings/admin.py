from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "room",
        "check_in",
        "check_out",
        "guest",
    )
    list_filter = ("kind",)


# Register your models here.

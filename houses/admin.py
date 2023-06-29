from django.contrib import admin
from .models import House


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "address",
        "price",
        "description",
    ]
    list_filter = ["name", "price"]
    search_fields = ["address"]


# Register your models here.

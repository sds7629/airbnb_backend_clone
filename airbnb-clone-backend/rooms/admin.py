from django.contrib import admin
from .models import Room, Amenity


@admin.action(description="Set all Price Zero")
def reset_price(model_admin, request, rooms):
    for room in rooms.all():
        room.price = 0
        room.save()

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    actions = (reset_price,)
    list_display = (
        "name",
        "price",
        "kind",
        "total_amenities",
        "owner",
        "rating",
    )
    list_filter = (
        "country",
        "city",
        "pet_friendly",
        "kind",
        "amenities",
        "updated_at",
    )
 
    search_fields = (
        "name",
        "price",
    )

    # def total_amenities(self, room):  # admin page에 ORM으로 amenity의 개수를 나타내주는 코드
    #     return room.amenities.count()  # model의 total_amenities 메서드와 결과값이 같다.


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )


# Register your models here.

from django.db import models
from common.models import CommonModel


class Room(CommonModel):
    """
    Room model
    """

    class RoomKindChoices(models.TextChoices):
        ENTIRE_PLACE = ("entire_place", "Entir_place")
        PRIVATE_ROOM = ("private_room", "Private_room")
        SHARED_ROOM = ("shared_room", "Shared_room")

    name = models.CharField(max_length=180, default="")
    country = models.CharField(max_length=50, default="Korea")
    city = models.CharField(max_length=80, default="Seoul")
    price = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    toilets = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=250)
    pet_friendly = models.BooleanField(default=True)
    kind = models.CharField(
        max_length=20,
        choices=RoomKindChoices.choices,
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="rooms",
    )
    amenities = models.ManyToManyField("rooms.Amenity")
    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name = "rooms",
    )

    def __str__(self):
        return self.name

    def total_amenities(self):
        return self.amenities.count()
    
    def rating(self):
        count =  self.reviews.count()
        if count == 0:
            return "No Reviews"
        else:
            total_rating = 0
            for review in self.reviews.all().values("rating"):
              total_rating += review["rating"]
            return round(total_rating / count,2)


class Amenity(CommonModel):
    """
    Amenity Model
    """

    name = models.CharField(max_length=150)
    description = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Amenities"


# Create your models here.

from django.db import models
from common.models import CommonModel


class Experience(CommonModel):
    """
    Experience Model
    """

    country = models.CharField(
        max_length=50,
        default="Korea",
    )
    city = models.CharField(
        max_length=80,
        default="Seoul",
    )
    name = models.CharField(
        max_length=250,
    )
    host = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name = "experiences",
    )
    price = models.PositiveIntegerField()
    address = models.CharField(
        max_length=250,
    )
    start = models.TimeField()
    end = models.TimeField()
    description = models.TextField()
    perks = models.ManyToManyField("experiences.Perk",related_name = "experiences",)
    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name = "experiences",
    )

    def __str__(self):
        return self.name


class Perk(CommonModel):
    """
    Perks = What is included on an Experience
    """

    name = models.CharField(
        max_length=100,
    )
    details = models.CharField(
        max_length=250,
        default="",
        blank=True,
    )
    explanation = models.TextField(
        default="",
        blank=True,
    )

    def __str__(self):
        return self.name


# Create your models here.

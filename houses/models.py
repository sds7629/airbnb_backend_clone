from django.db import models


class House(models.Model):
    name = models.CharField(max_length=140)
    price = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=140)
    pets_allowed = models.BooleanField(
        verbose_name="Pets Allowed?",
        default=True,
        help_text="Does this house allow pets?",
    )

    def __str__(self):
        return self.name


# Create your models here.

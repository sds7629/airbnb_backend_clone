from django.contrib import admin
from .models import Review


class WordFilter(admin.SimpleListFilter):
    title = "Filter by words and Rating"

    parameter_name = "reviews"

    def lookups(self, request, model_admin):
        return [
            ("bad", "Bad is lt 3"),
            ("good", "Good is gte 3"),
        ]
    def queryset(self, request, reviews):
        word = self.value()
        if word == "bad":
            return reviews.filter(rating__lt = 3)
        elif word == "good":
            return reviews.filter(rating__gte = 3)
        else:
            return reviews

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "payload",
    )
    list_filter = (
        WordFilter,
        "rating",
        "user__is_host",
        "room__category",
        "room__pet_friendly",)

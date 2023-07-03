from django.shortcuts import render
from django.http import HttpResponse
from .models import Room

def see_all_room(request):
    rooms = Room.objects.all()
    return render(
        request, "all_rooms.html",{"rooms": rooms, "title": "Hello! this title comes from django",}
    )
def see_one_room(request, room_id):
    return HttpResponse("see room id: "f"{room_id}") 
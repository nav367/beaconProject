import datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from beaconProject.core.models import MeetingRoom, Presence


@login_required
def home(request):
    return render(request, "base.html", context={})

@login_required()
def add_presence_log(request):
    user_email = request.GET.get('user')
    beacon_id = request.GET.get('beacon')
    meeting_room = MeetingRoom.objects.get(beacon_id=beacon_id)
    user = User.objects.get(email=user_email)
    Presence.objects.create(meeting_room=meeting_room, user=user, timestamp=datetime.datetime.now)
    return render(request, "base.html", context={})

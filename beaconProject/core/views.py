import datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from beaconProject.core.models import MeetingRoom, Presence
from beaconProject.settings import USER_PRESENCE_TIMESTAMP, USER_PRESENCE_END_TIMESTAMP


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


def update_presence_log(request):
    data = {
        "user_id": 1,
        "beacon_id": 1
    }
    timestamp = datetime.datetime.now() - datetime.timedelta(seconds=USER_PRESENCE_TIMESTAMP)
    user = User.objects.get(id=data['user_id'])
    meeting_room = MeetingRoom.objects.get(beacon_id=data['beacon_id'])
    logs = Presence.objects.filter(user=user,
                                   in_time__gte=timestamp)
    if not logs:
        Presence.objects.create(user=user,
                                meeting_room=meeting_room,
                                timestamp=datetime.datetime.now(),
                                in_time=datetime.datetime.now(),
                                out_time=None)
    else:
        logs.update(timestamp=datetime.datetime.now())
    return HttpResponse(status=200)


def update_presence_log_on_end_meeting(request):
    timestamp = datetime.datetime.now() - datetime.timedelta(seconds=USER_PRESENCE_END_TIMESTAMP)
    logs = Presence.objects.filter(timestamp__lte=timestamp, out_time__isnull=True)
    logs.update(out_time=datetime.datetime.now())
    return HttpResponse(status=200)

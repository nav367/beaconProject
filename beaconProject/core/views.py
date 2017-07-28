import datetime
import pytz
from dateutil import tz
from dateutil.tz import tzutc
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from beaconProject.core.calendar_events import event_lister
from beaconProject.core.models import MeetingRoom, Presence
from beaconProject.settings import USER_PRESENCE_TIMESTAMP, USER_PRESENCE_END_TIMESTAMP


@login_required
def home(request):
    meeting_room = MeetingRoom.objects.get(name="godfather")
    start = datetime.datetime(2017, 7, 27, 0, 0, tzinfo=tzutc())
    end = datetime.datetime(2017, 7, 28, 23, 50, tzinfo=tzutc())
    event_lister.get_events(meeting_room.room_resource_id, start, end)
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


def get_meeting_room_status(request):
    presence_logs = Presence.objects.select_related('meeting_room').exclude(out_time__isnull=True)
    presence_set = set()
    room_details = []
    for log in presence_logs:
        presence_set.add(log.meeting_room.name)
    meeting_rooms = MeetingRoom.objects.all()
    for room in meeting_rooms:
        if room.name in list(presence_set):
            room_details.append({'availability': 1, 'details': room})
        else:
            room_details.append({'availability': 0, 'details': room})
    return render(request, "base.html", context={'meeting_rooms': room_details})

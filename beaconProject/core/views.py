import datetime
import pytz
from dateutil import tz
from dateutil.tz import tzutc
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from beaconProject.core.calendar_events import event_lister
from beaconProject.core.models import MeetingRoom, Presence, Meeting
from beaconProject.settings import USER_PRESENCE_TIMESTAMP, USER_PRESENCE_END_TIMESTAMP


@login_required
def home(request):
    meeting_room = MeetingRoom.objects.get(name="godfather")
    start = datetime.datetime(2017, 7, 27, 0, 0, tzinfo=tzutc())
    end = datetime.datetime(2017, 7, 28, 23, 50, tzinfo=tzutc())
    event_lister.get_events(meeting_room.room_resource_id, start, end)
    return render(request, "base.html", context={})


def update_presence_log(request):
    # data = {
    #     "user_id": 1,
    #     "beacon_id": 1
    # }
    user_id = request.POST.get('user_id')
    beacon_id = request.POST.get('beacon_id')
    timestamp = datetime.datetime.now() - datetime.timedelta(seconds=USER_PRESENCE_TIMESTAMP)
    user = User.objects.get(email=user_id)
    meeting_room = MeetingRoom.objects.get(beacon_id=beacon_id)
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
    presence_logs = Presence.objects.select_related('meeting_room').filter(
        timestamp__gte=datetime.datetime(2017, 7, 28, 0, 0, tzinfo=tzutc()) - datetime.timedelta(seconds=USER_PRESENCE_TIMESTAMP), out_time__isnull=True)
    presence_set = set()
    room_details = []
    all_rooms = MeetingRoom.objects.all()
    all_rooms_set = set(all_rooms)

    for log in presence_logs:
        presence_set.add(log.meeting_room)
    available_rooms = list(all_rooms_set-presence_set)
    for room in all_rooms:
        if room in available_rooms:
            room_details.append({'availability': 1, 'details': room})
        else:
            room_details.append({'availability': 0, 'details': room})
    return render(request, "base.html", context={'meeting_rooms': room_details})

def get_timing_for_user(meeting):
    meeting = Meeting.objects.get(id=meeting.id)
    users = meeting.user.all()
    users_presence = []
    for user in users:
        presence = Presence.objects.filter(user=user, meeting_room=meeting.meeting_room_id,
                                           in_time__range=(meeting.start_time,meeting.end_time))
        
        if presence:
            late_time = presence[0].in_time-meeting.start_time
            late_time = ((late_time.seconds//60)%60)
            if  late_time>0:
                users_presence.append({'user':user, 'presence':'{0} mins late'.format(late_time)})
            else:
                users_presence.append({'user': user, 'presence': 'On Time'})
        else:
            users_presence.append({'user': user, 'presence': 'Absent'})
    return users_presence


def get_meeting_reports(request):
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    all_meetings = Meeting.objects.filter(start_time__range=(today_min, today_max), end_time__range=(today_min, today_max))
    meeting_data = []
    for meeting in all_meetings:
        meeting_data.append({'start_time':meeting.start_time.time(),
                             'end_time':meeting.end_time.time(),
                             'id': meeting.meeting_id,
                             'presence':get_timing_for_user(meeting)})
    
    return render(request, "reports.html", context={'meetings':meeting_data})

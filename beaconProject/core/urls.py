from django.conf.urls import url

from .views import home, update_presence_log, get_meeting_room_status, get_meeting_reports, get_report_home

urlpatterns = [
    url(r'^home/', home),
    url(r'^update_presence_log/', update_presence_log),
    url(r'get-meeting-rooms/',get_meeting_room_status),
    url(r'^get-meetings', get_meeting_reports),
    url(r'^view-reports/', get_report_home),
]

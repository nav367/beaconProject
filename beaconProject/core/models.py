from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class MeetingRoom(models.Model):
    name = models.CharField(max_length=20)
    beacon_id = models.CharField(max_length=10)
    room_resource_id = models.CharField(max_length=100, null=True, blank=True)
    floor = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self):
        return self.name


class Meeting(models.Model):
    meeting_id = models.CharField(max_length=15)
    user = models.ManyToManyField(User)
    meeting_room_id = models.ForeignKey(MeetingRoom)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


class Presence(models.Model):
    user = models.ForeignKey(User)
    meeting_room = models.ForeignKey(MeetingRoom)
    timestamp = models.DateTimeField()
    in_time = models.DateTimeField(null=True, blank=True)
    out_time = models.DateTimeField(null=True, blank=True)
    planned_meeting = models.BooleanField(default=False)

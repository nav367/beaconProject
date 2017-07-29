from django.contrib import admin

# Register your models here.
from .models import *

class PresenceAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'in_time', 'out_time', 'user', 'meeting_room']

admin.site.register(Meeting)
admin.site.register(MeetingRoom)
admin.site.register(Presence, PresenceAdmin)
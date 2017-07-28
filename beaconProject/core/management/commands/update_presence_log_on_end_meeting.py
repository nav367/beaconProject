import datetime
from django.core.management.base import BaseCommand

from beaconProject.core.models import Presence
from beaconProject.settings import USER_PRESENCE_END_TIMESTAMP


class Command(BaseCommand):
    def handle(self, *args, **options):
        timestamp = datetime.datetime.now() - datetime.timedelta(seconds=USER_PRESENCE_END_TIMESTAMP)
        logs = Presence.objects.filter(timestamp__lte=timestamp, out_time__isnull=True)
        logs.update(out_time=datetime.datetime.now())
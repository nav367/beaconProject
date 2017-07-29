import requests
from django.conf import settings



class EventLister:

    CALENDAR_API = "https://www.googleapis.com/calendar/v3/calendars/{0}/events?timeMax={1}&timeMin={2}&key=AIzaSyDuOu2zV6Fff-wRe60z2CMn1iaCTQR8Gw0"

    # def __init__(self, api_key):
    #     self.api_key = api_key

    def get_events(self, room_id, start_time, end_time):
        """
        function to get events between start and end time provided
        """
        event_response = requests.get(self.CALENDAR_API.format(room_id,start_time,end_time)).json()
        return event_response


event_lister = EventLister()

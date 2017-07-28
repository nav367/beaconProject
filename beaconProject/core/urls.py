from django.conf.urls import url

from .views import home, update_presence_log

urlpatterns = [
    url(r'^home/', home),
    url(r'^update_presence_log/', update_presence_log)
]

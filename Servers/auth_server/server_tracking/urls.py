from django.conf.urls import url, include
from django.contrib import admin

from server_tracking.views import ClientServerCrudApiView

urlpatterns = [
    url(r'^api/$', ClientServerCrudApiView.as_view(), name="client_server_crud"),
]

from django.urls import path
from . import views

urlpatterns = [
    path("send/", views.upload_screenshot, name="upload_screenshot"),
    path("share/<uuid:uuid>/", views.get_screenshot, name="get_screenshot"),
]

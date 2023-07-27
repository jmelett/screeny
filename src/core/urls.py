from django.urls import path
from .views import HomeView, upload_screenshot, get_screenshot

urlpatterns = [
    path('', HomeView.as_view(), name='screeny_project_root'), 
    path("send/", upload_screenshot, name="upload_screenshot"),
    path("share/<uuid:uuid>/", get_screenshot, name="get_screenshot"),
]

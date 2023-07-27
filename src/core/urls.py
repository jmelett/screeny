from django.urls import path
from .views import HomeView,  ScreenshotDetailView, upload_screenshot

urlpatterns = [
    path('', HomeView.as_view(), name='screeny_project_root'), 
    path("send/", upload_screenshot, name="upload_screenshot"),
    path("share/<uuid:uuid>/",  ScreenshotDetailView.as_view(), name="get_screenshot"),
]

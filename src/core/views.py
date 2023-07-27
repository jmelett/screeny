import os
import requests
from wsgiref.util import FileWrapper

from django.conf import settings
from django.db.models import F
from django.http import FileResponse, Http404, HttpResponse, StreamingHttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import TemplateView, DetailView

from rest_framework.decorators import api_view
from .models import Screenshot


class FileResponseWithClose(FileResponse):
    def __init__(self, *args, **kwargs):
        self.file_to_stream = kwargs.pop("file", None)
        super().__init__(*args, **kwargs)

    def close(self):
        if not self.closed and self.file_to_stream is not None:
            self.file_to_stream.close()
        super().close()


class HomeView(TemplateView):
    template_name = "base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ScreenshotDetailView(DetailView):
    model = Screenshot
    template_name = "core/share_image.html"

    def get_object(self):
        # Overriding get_object to use uuid instead of default pk
        uuid = self.kwargs.get("uuid")
        return get_object_or_404(Screenshot, uuid=uuid)

    def get(self, request, *args, **kwargs):
        # Override the get method to increase the views count
        self.object = self.get_object()
        Screenshot.objects.filter(uuid=self.object.uuid).update(views=F("views") + 1)
        self.object.refresh_from_db()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


@api_view(["POST"])
def upload_screenshot(request):
    if "file" not in request.FILES:
        return HttpResponse(
            "ERR: No file received", content_type="text/plain", status=400
        )

    file = request.FILES["file"]
    image = Screenshot(image=file, original_filename=file.name)
    image.save()

    image_url = request.build_absolute_uri(
        reverse("get_screenshot", kwargs={"uuid": image.uuid})
    )
    return HttpResponse(f"SUCCESS: {image_url}", content_type="text/plain")


@api_view(["GET"])
def get_screenshot_reverse(request, uuid):
    screenshot = get_object_or_404(Screenshot, uuid=uuid)
    screenshot.views += 1
    screenshot.save()

    if settings.DEFAULT_STORAGE_DSN.startswith("file://"):
        # If using local storage, open the file directly.
        file = open(screenshot.image.path, "rb")
        response = FileResponse(file)

    else:
        # If using S3 or another cloud storage, download the file.
        image_url = screenshot.image.url
        response = requests.get(image_url, stream=True)
        response = StreamingHttpResponse(
            FileWrapper(response.raw), content_type="image/*"
        )

    return response

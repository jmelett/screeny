import os

from django.conf import settings
from django.db.models import F
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView

from rest_framework.decorators import api_view
from .models import Screenshot


class HomeView(TemplateView):
    template_name = "base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

class FileResponseWithClose(FileResponse):
    def __init__(self, *args, **kwargs):
        self.file_to_stream = kwargs.pop("file", None)
        super().__init__(*args, **kwargs)

    def close(self):
        if not self.closed and self.file_to_stream is not None:
            self.file_to_stream.close()
        super().close()


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
def get_screenshot(request, uuid):
    screenshot = get_object_or_404(Screenshot, uuid=uuid)
    screenshot.views = F("views") + 1
    screenshot.save()

    image_path = screenshot.image.path
    file = open(image_path, "rb")
    return FileResponseWithClose(file, file=file)

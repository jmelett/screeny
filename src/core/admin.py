from django.contrib import admin
from .models import Screenshot


class ScreenshotAdmin(admin.ModelAdmin):
    list_display = ("uuid", "original_filename", "views")
    readonly_fields = ("uuid", "original_filename", "views")


admin.site.register(Screenshot, ScreenshotAdmin)

import uuid
from datetime import timedelta
from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator


class TimeStampedUUIDModel(models.Model):
    """
    An abstract base class model that provides an ``uuid`` and self- updating
     ``created`` / ``modified`` fields.
    """

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def get_upload_to(instance, filename):
    uuid_filename = f"{instance.uuid}.{filename.split('.')[-1]}"
    return f"images/{uuid_filename}"


class Screenshot(TimeStampedUUIDModel):
    image = models.ImageField(upload_to=get_upload_to)
    original_filename = models.CharField(max_length=255, blank=True)
    views = models.PositiveIntegerField(default=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Capture the original file name on initialization before it's changed.
        if self.image:
            self.original_filename = self.image.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # TODO Delete file(s) properly before the db object is removed
        # self.image.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.image.url

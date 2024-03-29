# Generated by Django 4.2.3 on 2023-07-27 04:21

import core.models
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_content_content_url_alter_content_type"),
    ]

    operations = [
        migrations.CreateModel(
            name="Screenshot",
            fields=[
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("image", models.ImageField(upload_to=core.models.get_upload_to)),
                ("original_filename", models.CharField(blank=True, max_length=255)),
                ("views", models.PositiveIntegerField(default=0)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.DeleteModel(
            name="Content",
        ),
    ]

# Generated by Django 4.2.3 on 2023-07-19 09:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="content",
            name="content_url",
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name="content",
            name="type",
            field=models.CharField(
                choices=[
                    ("about", "About"),
                    ("releases", "Releases"),
                    ("news", "News"),
                ],
                max_length=255,
            ),
        ),
    ]
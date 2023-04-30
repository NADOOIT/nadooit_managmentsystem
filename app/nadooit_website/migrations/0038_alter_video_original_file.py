# Generated by Django 4.1.3 on 2023-04-27 09:03

from django.db import migrations, models
import nadooit_website.models


class Migration(migrations.Migration):

    dependencies = [
        ("nadooit_website", "0037_videoresolution_hls_playlist_file"),
    ]

    operations = [
        migrations.AlterField(
            model_name="video",
            name="original_file",
            field=models.FileField(
                storage=nadooit_website.models.RenameFileStorage(),
                upload_to="original_videos/",
            ),
        ),
    ]
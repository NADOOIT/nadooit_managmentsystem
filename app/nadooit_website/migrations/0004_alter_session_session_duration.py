# Generated by Django 4.1.3 on 2023-04-01 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nadooit_website", "0003_section_transition_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="session",
            name="session_duration",
            field=models.IntegerField(default=0),
        ),
    ]

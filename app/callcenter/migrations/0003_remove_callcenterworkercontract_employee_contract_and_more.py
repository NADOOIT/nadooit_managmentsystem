# Generated by Django 4.1.3 on 2023-05-09 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("callcenter", "0002_meetingrequest"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="callcenterworkercontract",
            name="employee_contract",
        ),
        migrations.RemoveField(
            model_name="meetingrequest",
            name="session",
        ),
        migrations.RemoveField(
            model_name="meetingrequest",
            name="user",
        ),
        migrations.DeleteModel(
            name="CallCenterManagerContract",
        ),
        migrations.DeleteModel(
            name="CallCenterWorkerContract",
        ),
        migrations.DeleteModel(
            name="MeetingRequest",
        ),
    ]

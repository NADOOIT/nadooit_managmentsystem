# Generated by Django 4.1.3 on 2023-04-10 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nadooit_website", "0017_alter_session_session_score"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="session_signals",
            name="total_interaction_time",
        ),
        migrations.AddField(
            model_name="session",
            name="total_interaction_time",
            field=models.FloatField(default=0),
        ),
    ]

# Generated by Django 4.1.9 on 2023-06-19 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_management', '0012_message_reply_markup'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='parse_mode',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]

# Generated by Django 4.1.9 on 2023-06-26 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot_management', '0015_chat_all_members_are_administrators_chat_title_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhotoMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.TextField(blank=True, null=True)),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot_management.message')),
            ],
        ),
    ]
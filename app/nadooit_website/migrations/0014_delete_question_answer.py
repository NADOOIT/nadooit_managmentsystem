# Generated by Django 4.1.3 on 2023-04-08 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("nadooit_website", "0013_question_answer"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Question_Answer",
        ),
    ]
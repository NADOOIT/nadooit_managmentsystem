# Generated by Django 4.1.3 on 2023-04-01 15:33

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("nadooit_website", "0002_section_section_transition_test_session"),
    ]

    operations = [
        migrations.CreateModel(
            name="Section_Transition",
            fields=[
                (
                    "section_transition_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("section_1_id", models.UUIDField()),
                ("section_2_id", models.UUIDField()),
                ("transition_percentage", models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name="section_transition_test",
            name="section_1_id",
        ),
        migrations.RemoveField(
            model_name="section_transition_test",
            name="section_2_id",
        ),
        migrations.RemoveField(
            model_name="section_transition_test",
            name="section_test_time",
        ),
        migrations.RemoveField(
            model_name="section_transition_test",
            name="transition_percentage",
        ),
        migrations.RemoveField(
            model_name="session",
            name="session_end_time",
        ),
        migrations.AddField(
            model_name="section_transition_test",
            name="section_was_pased",
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name="Section_Competition",
            fields=[
                (
                    "section_competition_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("section_competition_date", models.DateTimeField(auto_now_add=True)),
                (
                    "section_1_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="nadooit_website.section",
                    ),
                ),
                (
                    "section_transition_tests",
                    models.ManyToManyField(
                        to="nadooit_website.section_transition_test"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="section_transition_test",
            name="section_transition_id",
            field=models.ForeignKey(
                default=123,
                on_delete=django.db.models.deletion.CASCADE,
                to="nadooit_website.section_transition",
            ),
            preserve_default=False,
        ),
    ]

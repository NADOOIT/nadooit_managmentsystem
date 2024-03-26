# Generated by Django 4.1.13 on 2024-03-02 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('nadooit_hr', '0001_initial'),
        ('nadoo_complaint_management', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='customer_program_execution_manager',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='nadooit_hr.employee'),
        ),
    ]

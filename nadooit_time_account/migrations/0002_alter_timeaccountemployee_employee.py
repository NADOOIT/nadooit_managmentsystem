# Generated by Django 4.0.7 on 2022-08-26 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nadooit_hr', '0001_initial'),
        ('nadooit_time_account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeaccountemployee',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nadooit_hr.employee'),
        ),
    ]

# Generated by Django 4.1.2 on 2022-11-01 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nadooit_program_ownership_system', '0010_rename_nadooitprogramshare_programshare'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerprogram',
            name='price_per_hour_in_cent',
            field=models.IntegerField(default=0),
        ),
    ]
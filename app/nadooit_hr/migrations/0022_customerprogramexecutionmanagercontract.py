# Generated by Django 4.1.2 on 2022-11-07 11:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nadooit_hr', '0021_customermanagercontract_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerProgramExecutionManagerContract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('can_create_customer_program_execution', models.BooleanField(default=False)),
                ('can_delete_customer_program_execution', models.BooleanField(default=False)),
                ('can_give_manager_role', models.BooleanField(default=False)),
                ('contract', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='nadooit_hr.employeecontract')),
            ],
        ),
    ]
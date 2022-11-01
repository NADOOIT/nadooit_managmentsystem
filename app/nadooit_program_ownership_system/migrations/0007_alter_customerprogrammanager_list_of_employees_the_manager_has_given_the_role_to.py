# Generated by Django 4.1.2 on 2022-10-31 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nadooit_hr', '0004_rename_customers_the_manager_is_responsible_for_employeemanager_list_of_customers_the_manager_is_res'),
        ('nadooit_program_ownership_system', '0006_customerprogrammanager_list_of_employees_the_manager_has_given_the_role_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerprogrammanager',
            name='list_of_employees_the_manager_has_given_the_role_to',
            field=models.ManyToManyField(blank=True, related_name='list_of_employees_the_customer_program_manager_has_given_the_role_to', to='nadooit_hr.employee'),
        ),
    ]

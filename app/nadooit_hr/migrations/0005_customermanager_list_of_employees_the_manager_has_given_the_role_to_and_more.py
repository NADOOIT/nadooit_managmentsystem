# Generated by Django 4.1.2 on 2022-10-31 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nadooit_hr', '0004_rename_customers_the_manager_is_responsible_for_employeemanager_list_of_customers_the_manager_is_res'),
    ]

    operations = [
        migrations.AddField(
            model_name='customermanager',
            name='list_of_employees_the_manager_has_given_the_role_to',
            field=models.ManyToManyField(blank=True, related_name='list_of_employees_the_customer_manager_has_given_the_role_to', to='nadooit_hr.employee'),
        ),
        migrations.AddField(
            model_name='employeemanager',
            name='list_of_employees_the_manager_has_given_the_role_to',
            field=models.ManyToManyField(blank=True, related_name='list_of_employees_the_employee_manager_has_given_the_role_to', to='nadooit_hr.employee'),
        ),
    ]

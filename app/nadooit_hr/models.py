import uuid
from datetime import datetime
from email.policy import default

from django.db import models
from nadooit_auth.models import User
from nadooit_crm.models import Customer

# Create your models here.

# model for an employee
# an employee can work for multiple customers
# the relationship between an employee and a customer is defined by the EmployeeContract model
class Employee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # a customers field that shows what customers the employee is assigned to
    # customers_the_employee_works_for = models.ManyToManyField(Customer)

    created_at = models.DateTimeField(auto_now_add=True, editable=True)
    updated_at = models.DateTimeField(auto_now=True, editable=True)

    def __str__(self):
        display_name = self.user.display_name
        if display_name is not None:
            return display_name
        username = self.user.username
        if username is not None:
            return username
        return self.user.user_code


class EmployeeContract(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # the employee that is assigned to the customer
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    # the start date of the contract
    start_date = models.DateField(auto_now_add=True)

    # the end date of the contract
    end_date = models.DateField(null=True, blank=True)

    # if false the contract is not active and hidden from the frontend
    is_active = models.BooleanField(default=True)

    # the date the contract was deactivated
    deactivation_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=True)
    updated_at = models.DateTimeField(auto_now=True, editable=True)

    def __str__(self):
        return f"Angestelltenvertrag zwischen: {self.employee} - {self.customer}"


class EmployeeManagerContract(models.Model):

    contract = models.OneToOneField(EmployeeContract, on_delete=models.CASCADE)

    # if true, the employee manager can assign employees to customers
    # TODO #104 rename to can_add_employees
    can_add_new_employee = models.BooleanField(default=False)

    # if true, the employee manager can remove employees from customers
    # TODO #108 rename to can_delete_employees
    can_delete_employee = models.BooleanField(default=False)

    # if true, the employee manager can give the role of employee manager to other employees
    # TODO #103 rename to can_create_employee_manager_contract
    can_give_manager_role = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, editable=True)
    updated_at = models.DateTimeField(auto_now=True, editable=True)

    def __str__(self) -> str:
        return f"Angestelltenverwaltervertrag zwischen: {self.contract.employee} - {self.contract.customer}"

    def get_abilities(self):
        return {
            "can_add_new_employee": self.can_add_new_employee,
            "can_delete_employee": self.can_delete_employee,
            "can_give_manager_role": self.can_give_manager_role,
        }


class CustomerProgramManagerContract(models.Model):

    contract = models.OneToOneField(EmployeeContract, on_delete=models.CASCADE)

    # if true, the employee manager can assign employees to customers
    can_create_customer_program = models.BooleanField(default=False)

    # if true, the employee manager can remove employees from customers
    can_delete_customer_program = models.BooleanField(default=False)

    # if true, the employee manager can give the role of employee manager to other employees
    # TODO #105 rename to can_create_customer_program_manager_contract
    can_give_manager_role = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, editable=True)
    updated_at = models.DateTimeField(auto_now=True, editable=True)

    def __str__(self) -> str:
        return f"Kundenprogrammeverwaltervertrag zwischen: {self.contract.employee} - {self.contract.customer}"

    def get_abilities(self):
        return {
            "can_create_customer_program": self.can_create_customer_program,
            "can_delete_customer_program": self.can_delete_customer_program,
            "can_give_manager_role": self.can_give_manager_role,
        }


class CustomerProgramExecutionManagerContract(models.Model):

    # TODO rename from single to plural

    contract = models.OneToOneField(EmployeeContract, on_delete=models.CASCADE)

    # If true the customer can create customer program executions
    can_create_customer_program_execution = models.BooleanField(default=False)

    # If true the customer can delete customer program executions
    can_delete_customer_program_execution = models.BooleanField(default=False)

    # If true the customer can give the rights to other users
    # TODO #106 rename to can_create_customer_program_execution_manager_contract
    can_give_manager_role = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Kundenprogrammausführungverwaltervertrag zwischen: {self.contract.employee} - {self.contract.customer}"

    def get_abilities(self):
        return {
            "can_create_customer_program_execution": self.can_create_customer_program_execution,
            "can_delete_customer_program_execution": self.can_delete_customer_program_execution,
            "can_give_manager_role": self.can_give_manager_role,
        }


class TimeAccountManagerContract(models.Model):

    contract = models.OneToOneField(EmployeeContract, on_delete=models.CASCADE)

    # If true the customer can create customer program executions
    can_create_time_accounts = models.BooleanField(default=False)

    # If true the customer can delete customer program executions
    can_delete_time_accounts = models.BooleanField(default=False)

    # If true the customer can give the rights to other users
    # TODO #107 rename to can_create_time_account_manager_contract
    can_give_manager_role = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Zeitkontoverwaltervertrag zwischen: {self.contract.employee} - {self.contract.customer}"

    def get_abilities(self):
        return {
            "can_create_time_accounts": self.can_create_time_accounts,
            "can_delete_time_accounts": self.can_delete_time_accounts,
            "can_give_manager_role": self.can_give_manager_role,
        }


class CustomerManagerContract(models.Model):

    contract = models.OneToOneField(EmployeeContract, on_delete=models.CASCADE)

    # if true, the employee manager can give the role of employee manager to other employees
    can_give_manager_role = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Kundenverwaltervertrag zwischen: {self.contract.employee} - {self.contract.customer}"

    def get_abilities(self):
        return {
            "can_give_manager_role": self.can_give_manager_role,
        }

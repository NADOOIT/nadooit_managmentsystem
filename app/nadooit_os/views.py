from django.utils import timezone
from django.shortcuts import render

# imoport for userforms

from django.http import HttpRequest, HttpResponseRedirect
from nadooit_api_key.models import NadooitApiKeyManager

from nadooit_auth.models import User

from nadooit_hr.models import Employee
from .forms import ApiKeyForm, ApiKeyManagerForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from nadooit_time_account.models import (
    get_time_as_string_in_hour_format_for_time_in_seconds_as_integer,
)

# model imports
from nadooit_program_ownership_system.models import NadooitCustomerProgram
from nadooit_time_account.models import CustomerTimeAccount
from nadooit_hr.models import Employee
from nadooit_api_key.models import NadooitApiKey
from nadooit_api_executions_system.models import CustomerProgramExecution

# Manager Roles
from nadooit_time_account.models import TimeAccountManager


from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required

# Tests for user roles
def user_is_Time_Account_Manager(user: User) -> bool:
    if hasattr(user.employee, "timeaccountmanager"):
        return True
    return False


def user_is_Api_Key_Manager(user: User) -> bool:
    if hasattr(user.employee, "nadooitapikeymanager"):
        return True
    return False


def user_is_Api_Key_Manager_and_can_give_ApiKeyManager_role(user: User) -> bool:
    if hasattr(user.employee, "nadooitapikeymanager"):
        if user.employee.nadooitapikeymanager.can_give_ApiKeyManager_role:
            return True
    return False


def user_is_Employee_Manager(user: User) -> bool:
    if hasattr(user.employee, "employeemanager"):
        return True
    return False


def user_is_Customer_Program_Manager(user: User) -> bool:
    if hasattr(user.employee, "nadooitcustomerprogrammanager"):
        return True
    return False


def user_is_Customer_Program_Execution_Manager(user: User) -> bool:
    if hasattr(user.employee, "customerprogramexecutionmanager"):
        return True
    return False


# Getting the user roles
# If new roles are added, they need to be added here
# this function uses the user_is_... functions above
def get_user_manager_roles(request: HttpRequest) -> dict:
    return {
        "is_time_account_manager": user_is_Time_Account_Manager(request.user),
        "is_api_key_manager": user_is_Api_Key_Manager(request.user),
        "is_employee_manager": user_is_Employee_Manager(request.user),
        "is_customer_program_manager": user_is_Customer_Program_Manager(request.user),
        "is_customer_program_execution_manager": user_is_Customer_Program_Execution_Manager(
            request.user
        ),
    }


# Create your views here.
# Main page of the nadooit_os
@login_required(login_url="/auth/login-user")
def index_nadooit_os(request: HttpRequest):

    return render(
        request,
        "nadooit_os/index.html",
        # context as dict
        # first item is page_title
        # dict from get_user_manager_roles is added
        {
            "page_title": "Nadooit OS",
            **get_user_manager_roles(request),
        },
    )


# Views for the time account system
@login_required(login_url="/auth/login-user")
@user_passes_test(user_is_Time_Account_Manager, login_url="/auth/login-user")
def customer_time_account_overview(request: HttpRequest):

    time_accounts_the_user_is_responsible_for = list(
        TimeAccountManager.objects.get(
            employee=Employee.objects.get(user=request.user)
        ).time_accounts.all()
    )
    list_of_customer_time_accounts = []
    for time_account in time_accounts_the_user_is_responsible_for:
        # get the customertimeaccount for the time account
        customer_time_account = CustomerTimeAccount.objects.get(
            time_account=time_account
        )
        list_of_customer_time_accounts.append(customer_time_account)

    # group the customer time accounts by customer and sum up the time balances
    # the dictionary will look like this:
    """ 
    {	
        customer1: {
            customer_time_accounts: [customer_time_account1, customer_time_account2],
            customer_time_account_total_time_balance: 123456
        },
        customer2: {	
            customer_time_accounts: [customer_time_account3, customer_time_account4],
            customer_time_account_total_time_balance: 123456
        }	
    }	
    

    """
    customer_time_accounts_grouped_by_customer = {}
    for customer_time_account in list_of_customer_time_accounts:
        if customer_time_account.customer in customer_time_accounts_grouped_by_customer:
            customer_time_accounts_grouped_by_customer[customer_time_account.customer][
                "customer_time_accounts"
            ].append(customer_time_account)
            customer_time_accounts_grouped_by_customer[customer_time_account.customer][
                "customer_time_account_total_time_balance"
            ] += customer_time_account.time_account.time_balance_in_seconds
        else:
            customer_time_accounts_grouped_by_customer[
                customer_time_account.customer
            ] = {
                "customer_time_accounts": [customer_time_account],
                "customer_time_account_total_time_balance": customer_time_account.time_account.time_balance_in_seconds,
            }

    print(customer_time_accounts_grouped_by_customer)

    # format the time balances first to int then using the get_time_as_string_in_hour_format_for_time_in_seconds_as_integer function
    for customer in customer_time_accounts_grouped_by_customer:
        customer_time_accounts_grouped_by_customer[customer][
            "customer_time_account_total_time_balance"
        ] = get_time_as_string_in_hour_format_for_time_in_seconds_as_integer(
            int(
                customer_time_accounts_grouped_by_customer[customer][
                    "customer_time_account_total_time_balance"
                ]
            )
        )

    # format the time balances for each customer time account
    for customer in customer_time_accounts_grouped_by_customer:
        for customer_time_account in customer_time_accounts_grouped_by_customer[
            customer
        ]["customer_time_accounts"]:
            customer_time_account.time_account.time_balance_in_seconds = (
                get_time_as_string_in_hour_format_for_time_in_seconds_as_integer(
                    int(customer_time_account.time_account.time_balance_in_seconds)
                )
            )

    return render(
        request,
        "nadooit_os/customer_time_account_overview.html",
        {
            "page_title": "Übersicht der Zeitkonten",
            "customer_time_accounts_grouped_by_customer": customer_time_accounts_grouped_by_customer,
            **get_user_manager_roles(request),
        },
    )


# Views for the customer program overview
@login_required(login_url="/auth/login-user")
@user_passes_test(
    user_is_Customer_Program_Execution_Manager, login_url="/auth/login-user"
)
def customer_order_overview(request: HttpRequest):

    # All orders for the current customer
    # orders are the executions of customerprograms

    # the employee is the logged in user
    employee = Employee.objects.get(user=request.user)

    # the list of customers that the time accounts that the employee is responsible for belong to
    # the list has for its first element the customer that the employee is responsible for
    # the list has for its second element the ccustomer programm execution for the customer that the employee is responsible for
    customers_the_user_is_responsible_for_and_the_customer_programm_executions = []

    for (
        customer_the_employe_works_for
    ) in employee.customers_the_employee_works_for.all():
        # list of customer programms with of the customer
        customer_programms = NadooitCustomerProgram.objects.filter(
            customer=customer_the_employe_works_for
        )
        # list of customer programm executions for the customer programm
        customer_programm_executions = list(
            CustomerProgramExecution.objects.filter(
                customer_program__in=customer_programms
            )
        )
        # add the customer and the customer programm execution to the list
        customers_the_user_is_responsible_for_and_the_customer_programm_executions.append(
            [customer_the_employe_works_for, customer_programm_executions]
        )

    # Multiple lists for the different order states
    # List one shows all orders for the current month
    # List shows all previous orders
    print(customers_the_user_is_responsible_for_and_the_customer_programm_executions)
    return render(
        request,
        "nadooit_os/customer_order_overview.html",
        {
            "page_title": "Übersicht der Buchungen",
            "customers_the_user_is_responsible_for_and_the_customer_programm_executions": customers_the_user_is_responsible_for_and_the_customer_programm_executions,
            **get_user_manager_roles(request),
        },
    )


# API KEYS Views
@login_required(login_url="/auth/login-user")
@user_passes_test(user_is_Api_Key_Manager, login_url="/auth/login-user")
def create_api_key(request: HttpRequest):
    submitted = False
    if request.method == "POST":
        form = ApiKeyForm(request.POST)
        if form.is_valid():
            new_api_key = NadooitApiKey(
                api_key=form.cleaned_data["api_key"],
                user=form.cleaned_data["user_code"],
                is_active=form.cleaned_data["is_active"],
            )
            new_api_key.updated_at = timezone.now()
            new_api_key.created_at = timezone.now()
            new_api_key.save()
            return HttpResponseRedirect(
                "/nadooit-os/api_key/create-api-key?submitted=True"
            )
    else:
        form = ApiKeyForm()
        if "submitted" in request.GET:
            submitted = True

    form = ApiKeyForm
    return render(
        request,
        "nadooit_os/api_key/create_api_key.html",
        {
            "form": form,
            "submitted": submitted,
            "page_title": "NADOOIT API KEY erstellen",
            **get_user_manager_roles(request),
        },
    )


@login_required(login_url="/auth/login-user")
def revoke_api_key(request: HttpRequest):

    submitted = False
    if request.method == "POST":
        # get list of all api keys that are active for the user and set them to inactive
        api_keys = NadooitApiKey.objects.filter(user=request.user, is_active=True)
        for api_key in api_keys:
            api_key.is_active = False
            api_key.save()
        return HttpResponseRedirect("/nadooit-os/revoke-api-key?submitted=True")
    else:
        if "submitted" in request.GET:
            submitted = True

    return render(
        request,
        "nadooit_os/api_key/revoke_api_key.html",
        {
            "submitted": submitted,
            "page_title": "NADOOIT API KEY löschen",
            **get_user_manager_roles(request),
        },
    )


@login_required(login_url="/auth/login-user")
@user_passes_test(
    user_is_Api_Key_Manager_and_can_give_ApiKeyManager_role,
    login_url="/auth/login-user",
)
def give_api_key_manager_role(request: HttpRequest):
    submitted = False
    if request.method == "POST":
        form = ApiKeyManagerForm(
            request.POST,
        )

        if form.is_valid():

            user_code = form.cleaned_data["user_code"]
            # get the employee object for the user
            employee = Employee.objects.get(user__user_code=user_code)

            customers_the_new_manager_is_responsible_for = request.POST.getlist(
                "customers"
            )
            can_create_api_key = form.cleaned_data["can_create_api_key"]
            can_delete_api_key = form.cleaned_data["can_delete_api_key"]
            can_give_ApiKeyManager_role = form.cleaned_data[
                "can_give_ApiKeyManager_role"
            ]

            # check if the user is already an NadooitApiKeyManager
            if user_is_Api_Key_Manager(employee.user):
                # if the employee is already an ApiKeyManager, update the existing ApiKeyManager object but only give more rights
                api_key_manager = NadooitApiKeyManager.objects.get(employee=employee)
                if can_create_api_key == True:
                    api_key_manager.can_create_api_key = True

                if can_delete_api_key == True:
                    api_key_manager.can_delete_api_key = True

                if can_give_ApiKeyManager_role == True:
                    api_key_manager.can_give_ApiKeyManager_role = True

                api_key_manager.save()

            else:

                # create new api key manager
                new_api_key_manager = NadooitApiKeyManager.objects.create(
                    employee=employee,
                    can_create_api_key=can_create_api_key,
                    can_delete_api_key=can_delete_api_key,
                    can_give_ApiKeyManager_role=can_give_ApiKeyManager_role,
                )

                # add the customers the new manager is responsible for
                for customer in customers_the_new_manager_is_responsible_for:
                    new_api_key_manager.customers_the_manager_is_responsible_for.add(
                        customer
                    )
                new_api_key_manager.save()

            return HttpResponseRedirect(
                "/nadooit-os/give-api-key-manager-role?submitted=True"
            )

    else:
        form = ApiKeyManagerForm(
            request.POST,
        )
        if "submitted" in request.GET:
            submitted = True

    form = ApiKeyManagerForm(
        request.POST,
    )

    customers_the_manager_is_responsible_for = (
        request.user.employee.nadooitapikeymanager.customers_the_manager_is_responsible_for.all()
    )

    return render(
        request,
        "nadooit_os/api_key/give_api_key_manager_role.html",
        {
            "page_title": "NADOOIT API KEY erstellen",
            "form": form,
            "submitted": submitted,
            "customers_the_manager_is_responsible_for": customers_the_manager_is_responsible_for,
            **get_user_manager_roles(request),
        },
    )

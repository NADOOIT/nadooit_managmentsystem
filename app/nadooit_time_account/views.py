from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from nadooit_time_account.models import CustomerTimeAccount
from nadooit_crm.models import Customer
from nadooit_program_ownership_system.models import NadooitCustomerProgram
from nadooit_time_account.models import (
    get_time_as_string_in_hour_format_for_time_in_seconds_as_integer,
)
from nadooit_hr.models import Employee
from nadooit_time_account.models import TimeAccountManager
from nadooit_time_account.logic import (
    get__total_of_all_customer_time_account_balances__for__user,
)
from nadooit_api_executions_system.models import CustomerProgramExecution

from django.contrib.auth.decorators import user_passes_test


def user_is_TimeAccountManager(user):
    if hasattr(user.employee, "timeaccountmanager"):
        return True
    return False


# Create your views here.
@login_required(login_url="/auth/login-user")
@user_passes_test(user_is_TimeAccountManager, login_url="/auth/login-user")
def customer_time_account_overview(request):

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
        "nadooit_time_account/customer_time_account_overview.html",
        {
            "page_title": "Übersicht der Zeitkonten",
            "customer_time_accounts_grouped_by_customer": customer_time_accounts_grouped_by_customer,
        },
    )


@login_required(login_url="/auth/login-user")
@user_passes_test(user_is_TimeAccountManager, login_url="/auth/login-user")
def customer_order_overview(request):

    # All orders for the current customer
    # orders are the executions of customerprograms

    # the employee is the logged in user
    employee = Employee.objects.get(user=request.user)

    # the list of customers that the time accounts that the employee is responsible for belong to
    # the list has for its first element the customer that the employee is responsible for
    # the list has for its second element the ccustomer programm execution for the customer that the employee is responsible for
    customers_the_user_is_responsible_for_and_the_customer_programm_executions = []

    for customer_the_employe_works_for in employee.customers.all():
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
        "nadooit_time_account/customer_order_overview.html",
        {
            "page_title": "Übersicht der Buchungen",
            "customers_the_user_is_responsible_for_and_the_customer_programm_executions": customers_the_user_is_responsible_for_and_the_customer_programm_executions,
        },
    )


@login_required(login_url="/auth/login-user")
def admin(request):
    return render(
        request,
        "nadooit_time_account/admin.html",
        {"page_title": "Übersicht der Zeitkonten"},
    )

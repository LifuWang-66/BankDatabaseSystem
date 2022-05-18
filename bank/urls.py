from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("admin/", views.admin_view, name="admin"),
    path("manager/", views.manager, name="manager"),
    path("customer_or_manager/", views.customer_or_manager, name="customer_or_manager"),
    path("customer/", views.customer, name="customer"),
    
    path("display_bank_stats/", views.display_bank_stats, name="display_bank_stats"),
    path("display_account_stats/", views.display_account_stats, name="display_account_stats"),
    path("display_corporation_stats/", views.display_corporation_stats, name="display_corporation_stats"),
    path("display_customer_stats/", views.display_customer_stats, name="display_customer_stats"),
    path("display_employee_stats/", views.display_employee_stats, name="display_employee_stats"),
    path("view_stats/", views.view_stats, name="view_stats"),
    
    path("create_bank/", views.create_bank, name="create_bank"),
    path("create_corporation/", views.create_corporation, name="create_corporation"),
    path("start_customer_role/", views.start_customer_role, name="start_customer_role"),
    path("create_fee/", views.create_fee, name="create_fee"),

    path("stop_customer_role/", views.stop_customer_role, name="stop_customer_role"),
    
    path("manage_accounts_admin/", views.manage_accounts_admin, name="manage_accounts"),
    path("manage_accounts_customer/", views.manage_accounts_customer, name="manage_accounts"),
    path("manage_users/", views.manage_users, name="manage_users"),
    path("manage_overdraft/", views.manage_overdraft, name="manage_overdraft"),
    path("remove_accounts_access/", views.remove_accounts_access, name="remove_accounts_access"),
    path("account_deposit/", views.account_deposit, name="account_deposit"),
    path("account_withdrawal/", views.account_withdrawal, name="account_withdrawal"),
    path("account_transfer/", views.account_transfer, name="account_transfer"),

    path("penalize_accounts/", views.penalize_accounts, name="penalize_accounts"),
    path("accrue_interest/", views.accrue_interest, name="accrue_interest"),
    path("pay_employees/", views.pay_employees, name="pay_employees"),

    path("start_employee_role/", views.start_employee_role, name="start_employee_role"),
    path("hire_worker/", views.hire_worker, name="hire_worker"),
    path("stop_employee_role/", views.stop_employee_role, name="stop_employee_role"),

    path("replace_manager/", views.replace_manager, name="replace_manager"),
]
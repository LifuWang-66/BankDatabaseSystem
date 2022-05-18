from django.shortcuts import redirect, render
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import *

from datetime import date


cursor = connection.cursor()
username = '' # this is perID in the person table
admin_list = None
manager_list = None
customer_list = None


def require_user_login():
    if username == '':
        return True


def require_admin_login():
    if admin_list is None or username not in admin_list:
        return True


# Create your views here.
def index(request):
    global username
    username = request.session['username']

    if require_user_login():
        return redirect('login')

    global admin_list
    cursor.execute("select * from system_admin")
    result = cursor.fetchall()
    result = [perid[0] for perid in result]
    admin_list = result

    global manager_list
    cursor.execute("select manager from bank")
    result = cursor.fetchall()
    result = [perid[0] for perid in result]
    manager_list = result

    global customer_list
    cursor.execute("select * from customer")
    result = cursor.fetchall()
    result = [perid[0] for perid in result]
    customer_list = result

    if username in admin_list:
        return redirect("admin")

    if username in manager_list:
        if username in customer_list:
            return redirect("customer_or_manager")
        else:
            return redirect("manager")
    elif username in customer_list:
        return redirect("customer")
    context = {
        "username": username
    }
    return render(request, "bank/index.html", context)


def admin_view(request):
    context = {
        "username": username
    }
    return render(request, "bank/admin.html", context)


def customer_or_manager(request):
    context = {
        "username": username
    }
    return render(request, "bank/customer_or_manager.html", context)


def manager(request):
    context = {
        "username": username
    }
    return render(request, "bank/manager.html", context)


def customer(request):
    context = {
        "username": username
    }
    return render(request, "bank/customer.html", context)


## Views for Display Stats
def view_stats(request):
    if require_admin_login():
        return redirect('login')
        
    return render(request, "bank/view_stats.html")


def display_bank_stats(request):
    cursor.execute("select * from display_bank_stats")
    result = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    context = {
        'results': result, 
        'columns': columns,
        'title': 'Display Bank Stats'
    }
    return render(request, 'bank/display_bank_stats.html', context)


def display_employee_stats(request):
    cursor.execute("select * from display_employee_stats")
    result = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    context = {
        'results': result, 
        'columns': columns,
        'title': 'Display Employee Stats'
    }
    return render(request, 'bank/display_bank_stats.html', context)


def display_account_stats(request):
    cursor.execute("select * from display_account_stats")
    result = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    context = {
        'results': result, 
        'columns': columns,
        'title': 'Display Account Stats'
    }
    return render(request, 'bank/display_bank_stats.html', context)

def display_corporation_stats(request):
    cursor.execute("select * from display_corporation_stats")
    result = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    context = {
        'results': result, 
        'columns': columns,
        'title': 'Display Corporation Stats'
    }
    return render(request, 'bank/display_bank_stats.html', context)

def display_customer_stats(request):
    cursor.execute("select * from display_customer_stats")
    result = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    context = {
        'results': result, 
        'columns': columns,
        'title': 'Display Customer Stats'
    }
    return render(request, 'bank/display_bank_stats.html', context)


## Views for Create
def create_bank(request):
    form = CreateBankForm(request.POST or None)
    if form.is_valid():
        query = "call create_bank('" + str(form.cleaned_data["ip_bankid"]) + "', '" + str(form.cleaned_data["ip_bankname"]) + "', '" + str(form.cleaned_data["ip_street"]) + "', '" + str(form.cleaned_data["ip_city"]) + "', '" + str(form.cleaned_data["ip_state"]) + "', '" + str(form.cleaned_data["ip_zip"]) + "', '" + str(form.cleaned_data["ip_resassets"]) + "', '" + str(form.cleaned_data["ip_corpid"]) + "', '" + str(form.cleaned_data["ip_manager"]) + "','" + str(form.cleaned_data["ip_bank_employee"]) + "')"
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) == 0:
            messages.success(request, "Success!")
        elif result[0][0] == 1:
            messages.error(request, "The manager/employee you selected is not available.")
        elif result[0][0] == 2:
            messages.error(request, "Bank ID already exists.")
        elif result[0][0] == 3:
            messages.error(request, "Bank Address already exists")
    
    context = {
        'form': form
    }
    return render(request, "bank/create_bank.html", context)


def create_corporation(request):
    form = CorporationCreationForm(request.POST or None)
    if form.is_valid():
        query = "call create_corporation('" + str(form.cleaned_data["ip_corpID"]) + "', '" + str(form.cleaned_data["ip_shortName"])  + "', '" + str(form.cleaned_data["ip_longName"])+ "', '" + str(form.cleaned_data["ip_resAssets"])+"')"
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) == 0:
            messages.success(request, "Success!")
        elif result[0][0] == 1:
            messages.error(request, "Corp ID already exists.")
        elif result[0][0] == 2:
            messages.error(request, "Short name already exists.")
        elif result[0][0] == 3:
            messages.error(request, "Long name already exists.")    
    context = {
        'form': form
    }
    return render(request, "bank/create_corporation.html", context)


def start_employee_role(request):
    form = StartEmployeeForm(request.POST or None)
    if form.is_valid():
        query = "call start_employee_role('" + str(form.cleaned_data["ip_perID"]) + "', '" + \
            str(form.cleaned_data["ip_taxID"]) + "', '" + str(form.cleaned_data["ip_firstName"]) + "', '" + \
            str(form.cleaned_data["ip_lastName"]) + "', '" + str(form.cleaned_data["ip_birthdate"]) + "', '" + \
            str(form.cleaned_data["ip_street"]) + "', '" + str(form.cleaned_data["ip_city"]) + "', '" + \
            str(form.cleaned_data["ip_state"]) + "', '" + str(form.cleaned_data["ip_zip"]) + "', '" + \
            str(form.cleaned_data["ip_dtJoined"]) + "', '" + str(form.cleaned_data["ip_salary"]) + "', '" + \
            str(form.cleaned_data["ip_payments"]) + "', '" + str(form.cleaned_data["ip_earned"]) + "', '" + \
            str(form.cleaned_data["emp_password"]) + "')"
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) == 0:
            messages.success(request, "Success!")
        elif result[0][0] == 1:
            messages.error(request, "The person is in the system already.")
        elif result[0][0] == 2:
            messages.error(request, "The person is an administrator.")
        elif result[0][0] == 3:
            messages.error(request, "Tax id already exists.")
    context = {
        'form': form
    }
    return render(request, "bank/start_employee_role.html", context)


def start_customer_role(request):
    form = StartCustomerForm(request.POST or None)
    if form.is_valid():
        query = "call start_customer_role('" + str(form.cleaned_data["ip_perID"]) + "', '" + \
            str(form.cleaned_data["ip_taxID"]) + "', '" + str(form.cleaned_data["ip_firstName"]) + "', '" + \
            str(form.cleaned_data["ip_lastName"]) + "', '" + str(form.cleaned_data["ip_birthdate"]) + "', '" + \
            str(form.cleaned_data["ip_street"]) + "', '" + str(form.cleaned_data["ip_city"]) + "', '" + \
                str(form.cleaned_data["ip_state"]) + "', '" + str(form.cleaned_data["ip_zip"]) + "', '" + \
                str(form.cleaned_data["ip_dtJoined"]) + "', '" + str(form.cleaned_data["ip_cust_password"]) + "')"
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) == 0:
            messages.success(request, "Success!")
        elif result[0][0] == 1:
            messages.error(request, "The person is an administrator.")
        elif result[0][0] == 2:
            messages.error(request, "The person is already a customer.")
        elif result[0][0] == 3:
            messages.error(request, "Tax id already exists.")
    context = {
        'form': form
    }
    return render(request, "bank/start_customer_role.html", context)


def stop_customer_role(request):
    form = StopCustomerForm(request.POST or None)
    if form.is_valid():
        query = "call stop_customer_role('" + str(form.cleaned_data["ip_perID"]) + "')"
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) == 0:
            messages.success(request, "Success!")
        elif result[0][0] == 1:
            messages.error(request, "The person is not a customer.")
        elif result[0][0] == 2:
            messages.error(request, "The customer is the only holder of an account, so we cannot remove the customer.")
    context = {
        'form': form
    }
    return render(request, "bank/stop_customer_role.html", context)


def stop_employee_role(request):
    form = StopEmployeeForm(request.POST or None)
    if form.is_valid():
        query = "call stop_employee_role('" + str(form.cleaned_data["ip_perID"]) + "')"
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) == 0:
            messages.success(request, "Success!")
        elif result[0][0] == 1:
            messages.error(request, "The person is not an employee.")
        elif result[0][0] == 2:
            messages.error(request, "The employee is a manager.")
        elif result[0][0] == 3:
            messages.error(request, "The employee is the last employee at a bank.")
    context = {
        'form': form
    }
    return render(request, "bank/stop_employee_role.html", context)


def penalize_accounts(request):
    query = "call penalize_accounts()"
    cursor.execute(query)
    messages.success(request, "Success!")
    return render(request, "bank/penalize_accounts.html")


def accrue_interest(request):
    query = "call accrue_interest()"
    cursor.execute(query)
    messages.success(request, "Success!")
    return render(request, "bank/accrue_interest.html")


# Views for Manage
def manage_accounts_admin(request):
    form = ManageAccountsAdminForm(request.POST or None)
    if form.is_valid():
        
        if form.cleaned_data["ip_interest_rate"] is None:
            ip_interest_rate = "null"
        else:
            ip_interest_rate = str(form.cleaned_data["ip_interest_rate"])
        
        if form.cleaned_data["ip_dt_deposit"] is None:
            ip_dt_deposit = "null"
        else:
            ip_dt_deposit = "'" + str(form.cleaned_data["ip_dt_deposit"]) + "'"
        
        if form.cleaned_data["ip_min_balance"] is None:
            ip_min_balance = "null"
        else:
            ip_min_balance = str(form.cleaned_data["ip_min_balance"])        
        
        if form.cleaned_data["ip_num_withdrawals"] is None:
            ip_num_withdrawals = "null"
        else:
            ip_num_withdrawals = str(form.cleaned_data["ip_num_withdrawals"])        
        
        if form.cleaned_data["ip_max_withdrawals"] is None:
            ip_max_withdrawals = "null"
        else:
            ip_max_withdrawals = str(form.cleaned_data["ip_max_withdrawals"])

        query = "call add_account_access('" + str(username) + "', '" + str(form.cleaned_data["ip_customer"]) + "', '" + \
            str(form.cleaned_data["ip_account_type"]) + "', '" + str(form.cleaned_data["ip_bankid"]) + "', '" + \
            str(form.cleaned_data["ip_accountid"]) + "', " + str(form.cleaned_data["ip_balance"]) + ", " + \
            ip_interest_rate + ", " + ip_dt_deposit + "," + ip_min_balance + "," + ip_num_withdrawals + "," + ip_max_withdrawals + ", '" + \
            str(form.cleaned_data["ip_dt_share_start"]) + "')"
        print(query)
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) == 0:
            messages.success(request, "Success!")
        elif result[0][0] == 1:
            messages.error(request, "The customer already has the access to the account.")
    context = {
        "form": form
    }
    return render(request, "bank/manage_accounts_admin.html", context)


def manage_users(request):
    return render(request, "bank/manage_users.html")


def manage_accounts_customer(request):
    form = ManageAccountsCustomerForm(request.POST or None, username=username)

    if form.is_valid():
        # if no access, leave
        today = date.today()
        date_str = today.strftime("%Y-%m-%d")
        query = "select * from access where accountID = '" + str(form.cleaned_data["ip_accountid"]) + "' and bankID = '" + \
            str(form.cleaned_data["ip_bankid"]) + "' and perID = '" + username + "'"
        print(query)
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) == 0:
            messages.success(request, "The account does not exist or not accessible.")
            context = {
                "form": form
            }
            return render(request, "bank/manage_accounts_customer.html", context)

        if form.cleaned_data["ip_add_owner"]:

            # if form.cleaned_data["ip_dt_share_start"] is None:
            #     messages.error(request, "Please enter \"Date Share Start\"!")
            #     context = {
            #         "form": form
            #     }
            #     return render(request, "bank/manage_accounts_customer.html", context)

            # determine account type
            query = "select * from checking where accountID = '" + str(form.cleaned_data["ip_accountid"]) + "' and bankID = '" + str(form.cleaned_data["ip_bankid"]) + "'"
            print(query)
            cursor.execute(query)
            result = cursor.fetchall()
            if len(result) != 0:
                account_type = "checking"
            else:
                query = "select * from savings where accountID = '" + str(form.cleaned_data["ip_accountid"]) + "' and bankID = '" + str(form.cleaned_data["ip_bankid"]) + "'"
                print(query)
                cursor.execute(query)
                result = cursor.fetchall()
                if len(result) != 0:
                    account_type = "savings"
                else:
                    account_type = "market"
            
            # actual call
            query = "call add_account_access('" + str(username) + "', '" + str(form.cleaned_data["ip_customer"]) + "', '" + \
                account_type + "', '" + str(form.cleaned_data["ip_bankid"]) + "', '" + str(form.cleaned_data["ip_accountid"]) + \
                "', null, null, null, null, null, null, '" + date_str + "')"
            
            print(query)
            cursor.execute(query)
            result = cursor.fetchall()
            if len(result) == 0:
                messages.success(request, "Success!")
            elif result[0][0] == 1:
                messages.error(request, "The customer already has access to the account.")
        
        else:
            query = "call remove_account_access('" + str(username) + "', '" + str(form.cleaned_data["ip_customer"]) + "', '" + \
                str(form.cleaned_data["ip_bankid"]) + "', '" + str(form.cleaned_data["ip_accountid"])  + "')"
            print(query)
            cursor.execute(query)
            messages.success(request, "Success!")

    context = {
        "form": form
    }
    return render(request, "bank/manage_accounts_customer.html", context)


def remove_accounts_access(request):
    form = RemoveAccountsAccessForm(request.POST or None)
    if form.is_valid():
        query = "select * from checking where accountID = '" + str(form.cleaned_data["ip_accountid"]) + "' and bankID = '" + str(form.cleaned_data["ip_bankid"]) + "'"
        print(query)
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) == 0:
            messages.success(request, "The account does not exist.")
            context = {
                "form": form
            }
            return render(request, "bank/remove_accounts_access.html", context)

        query = "call remove_account_access('" + str(username) + "', '" + str(form.cleaned_data["ip_customer"]) + "', '" + \
            str(form.cleaned_data["ip_bankid"]) + "', '" + str(form.cleaned_data["ip_accountid"])  + "')"
        print(query)
        cursor.execute(query)
        result = cursor.fetchall()
        messages.success(request, "Success!")
    
    context = {
        "form": form
    }
    return render(request, "bank/remove_accounts_access.html", context)



# Views for Account  
def account_withdrawal(request):
    form = AccountWithdrawalForm(request.POST or None, username=username)
    if form.is_valid():
        today = date.today()
        date_str = today.strftime("%Y-%m-%d")
        query = "call account_withdrawal('" + str(username) + "', '" + str(form.cleaned_data["ip_withdrawal_amount"]) + "', '" + str(form.cleaned_data["ip_bankid"]) + "', '" + str(form.cleaned_data["ip_accountid"]) + "', '" + date_str + "')"
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) == 0:
            messages.success(request, "Success!")
        elif result[0][0] == 1:
            messages.error(request, "No enough balance")

    context = {
        'form1': form
    }
    return render(request, "bank/account_withdrawal.html", context)


def account_transfer(request):
    form1 = AccountTransferForm(request.POST or None, username=username)
    if form1.is_valid():
        today = date.today()
        date_str = today.strftime("%Y-%m-%d")
        query = "call account_transfer('" + str(username) + "', '" + str(form1.cleaned_data["ip_transfer_amount"]) + "', '" + str(form1.cleaned_data["ip_from_bankid"]) + "', '" + str(form1.cleaned_data["ip_from_accountid"]) + "', '" + str(form1.cleaned_data["ip_to_bankid"]) + "', '" + str(form1.cleaned_data["ip_to_accountid"]) + "', '" + date_str + "')"
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) == 0:
            messages.success(request, "Success!")
        elif result[0][0] == 1:
            messages.error(request, "No enough balance")
    
    context = {
        'form1': form1,
    }
    return render(request, "bank/account_transfer.html", context)


def account_deposit(request):
    form = AccountDepositForm(request.POST or None, username=username)
    if form.is_valid():
        today = date.today()
        date_str = today.strftime("%Y-%m-%d")
        query = "call account_deposit('" + str(username) + "', '" + str(form.cleaned_data["ip_deposit_amount"]) + "', '" + str(form.cleaned_data["ip_bankid"]) + "', '" + str(form.cleaned_data["ip_accountid"]) + "', '" + date_str + "')"
        cursor.execute(query)
        messages.success(request, "Success!")

    context = {
        'form1': form
    }
    return render(request, "bank/account_deposit.html", context)


def create_fee(request):
    form = CreateFeeForm(request.POST or None)
    
    if form.is_valid():
        query = "call create_fee('" + str(form.cleaned_data["ip_bankid"]) + "', '" + str(form.cleaned_data["ip_accountid"]) + "', '" + str(form.cleaned_data["ip_fee_type"]) + "')"
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) == 0:
            messages.success(request, "Success!")
        elif result[0][0] == 1:
            messages.error(request, "Fee already exists.")
        elif result[0][0] == 2:
            messages.error(request, "Account does not exist.")
        elif result[0][0] == 3:
            messages.error(request, "Account is not an interest bearing account.")

    context = {
        'form': form
    }
    return render(request, "bank/create_fee.html", context)


def manage_overdraft(request):
    form = ManageOverdraftForm(request.POST or None)
    
    if form.is_valid():
        if form.cleaned_data["ip_add_overdraft"]: 
            query = "call start_overdraft('" + str(username) + "', '" + str(form.cleaned_data["ip_checking_bankid"]) + "', '" + str(form.cleaned_data["ip_checking_accountid"])  + "', '" + str(form.cleaned_data["ip_savings_bankid"])+ "', '" + str(form.cleaned_data["ip_savings_accountid"])+"')"
            cursor.execute(query)
            result = cursor.fetchall()
            if len(result) == 0:
                messages.success(request, "Success!")
            elif result[0][0] == 1:
                messages.error(request, "Checking account does not exists")
            elif result[0][0] == 2:
                messages.error(request, "Saving account does not exists")
            elif result[0][0] == 3:
                messages.error(request, "Saving account is already used for protection")
            elif result[0][0] == 4:
                messages.error(request, "Checking account is already protected")
        else:
            query = "call stop_overdraft('" + str(username) + "', '" + str(form.cleaned_data["ip_checking_bankid"]) + "', '" + str(form.cleaned_data["ip_checking_accountid"]) +"')"
            cursor.execute(query)
            result = cursor.fetchall()
            if len(result) == 0:
                messages.success(request, "Success!")
            elif result[0][0] == 1:
                messages.error(request, "Checking account does not exists")
            elif result[0][0] == 2:
                messages.error(request, "Checking account is not protected")

    context = {
        'form': form
    }
    return render(request, "bank/manage_overdraft.html", context)



def pay_employees(request):
    query = "call pay_employees()"
    cursor.execute(query)
    messages.success(request, "Success!")
    return render(request, "bank/pay_employees.html")


def replace_manager(request):
    form = ReplaceManagerForm(request.POST or None)
    if form.is_valid():
        query = "call replace_manager('" + str(form.cleaned_data["ip_perID"]) + "', '" +\
            str(form.cleaned_data["ip_bankID"]) + "', " + str(form.cleaned_data["ip_salary"]) + ")"
        print(query)
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) == 0:
            messages.success(request, "Success!")
        elif result[0][0] == 1:
            messages.error(request, "The person is not an employee.")
        elif result[0][0] == 2:
            messages.error(request, "The employee is already a manager")
        elif result[0][0] == 3:
            messages.error(request, "The employee is already a worker")
    context = {
        'form': form
    }
    return render(request, "bank/replace_manager.html", context)



def hire_worker(request):
    form = HireWorkerForm(request.POST or None)
    if form.is_valid(): 
        query = "call hire_worker('" + str(form.cleaned_data["ip_perid"]) + "', '"+ str(form.cleaned_data["ip_bankid"]) + "', '" + str(form.cleaned_data["ip_salary"]) + "')"
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) == 0:
            messages.success(request, "Success!")
        elif result[0][0] == 1:
            messages.error(request, "The person is not an employee.")
        elif result[0][0] == 2:
            messages.error(request, "The person is a manager.")
        elif result[0][0] == 3:
            messages.error(request, "The person already works in this bank.")
    context = {
        'form': form
    }
    return render(request, "bank/hire_worker.html", context)



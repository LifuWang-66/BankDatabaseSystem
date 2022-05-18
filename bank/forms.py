from dataclasses import field
from os import access
from django import forms
from .models import *


class CreateBankForm(forms.Form):
    ip_bankid = forms.CharField(label='Bank ID', max_length=100)
    ip_bankname = forms.CharField(label='Name', max_length=100)
    ip_street = forms.CharField(label='Street', max_length=100)
    ip_city = forms.CharField(label='City', max_length=100)
    ip_state = forms.CharField(label='State', max_length=2)
    ip_zip = forms.CharField(label='Zip', max_length=5)
    ip_resassets = forms.IntegerField(label='Reserved Assets')
    ip_corpid = forms.ChoiceField(label='Coporation ID', choices=[(i, i) for i in list(Corporation.objects.all().values_list('corpid', flat=True).distinct())])
    ip_manager = forms.ChoiceField(label='Manger', choices=[(i, i) for i in list(Employee.objects.all().values_list('perid', flat=True).distinct())])
    ip_bank_employee = forms.ChoiceField(label='Employee', choices=[(i, i) for i in list(Employee.objects.all().values_list('perid', flat=True).distinct())])



class CorporationCreationForm(forms.Form):
    ip_corpID = forms.CharField(label='Corporation ID', max_length=100)
    ip_shortName = forms.CharField(label='Short Name', max_length=100)
    ip_longName = forms.CharField(label='Long Name', max_length=100)
    ip_resAssets = forms.CharField(label='Reserved Assets', max_length=50)


class StartCustomerForm(forms.Form):
    ip_perID = forms.CharField(label='Person ID', max_length=100)
    ip_taxID = forms.CharField(label='Tax ID', max_length=11)
    ip_firstName = forms.CharField(label='First name', max_length=100)
    ip_lastName = forms.CharField(label='Last name', max_length=100)
    ip_birthdate = forms.CharField(label='Birthdate', max_length=100)
    ip_street = forms.CharField(label='Street', max_length=100)
    ip_city = forms.CharField(label='City', max_length=100)
    ip_state = forms.CharField(label='State', max_length=2)
    ip_zip = forms.CharField(label='Zip', max_length=5)
    ip_dtJoined = forms.CharField(label='Date joined', max_length=100)
    ip_cust_password = forms.CharField(label='Password', max_length=100)

class StopCustomerForm(forms.Form):
    ip_perID = forms.ChoiceField(label='Person ID', choices=[(i, i) for i in list(Customer.objects.all().values_list('perid', flat=True).distinct())])
    def __init__(self, *args, **kwargs):
        super(StopCustomerForm, self).__init__(*args, **kwargs)
        self.fields['ip_perID'] = forms.ChoiceField(label='Person ID', choices=[(i, i) for i in list(Customer.objects.all().values_list('perid', flat=True).distinct())])

class AccountTransferForm(forms.Form):
    ip_transfer_amount = forms.IntegerField(min_value=0)
    ip_from_bankid = forms.ChoiceField(label='Bank ID', choices=[(i, i) for i in list(Access.objects.all().values_list('bankid', flat=True).distinct())])
    ip_to_bankid = forms.ChoiceField(label='Bank ID', choices=[(i, i) for i in list(Access.objects.all().values_list('bankid', flat=True).distinct())])
    ip_from_accountid = forms.ChoiceField(label='Account ID', choices=[(i, i) for i in list(Access.objects.all().values_list('accountid', flat=True).distinct())])
    ip_to_accountid = forms.ChoiceField(label='Account ID', choices=[(i, i) for i in list(Access.objects.all().values_list('accountid', flat=True).distinct())])

    def __init__(self, *args, **kwargs):
        self._username = kwargs.pop('username', None)
        super(AccountTransferForm, self).__init__(*args, **kwargs)
        if self._username:
            self.fields['ip_from_bankid'] = forms.ChoiceField(label='Bank ID', choices=[(i, i) for i in list(Access.objects.filter(perid=self._username).values_list('bankid', flat=True).distinct())])
            self.fields['ip_from_accountid'] = forms.ChoiceField(label='Account ID', choices=[(i, i) for i in list(Access.objects.filter(perid=self._username).values_list('accountid', flat=True).distinct())])
            self.fields['ip_to_bankid'] = forms.ChoiceField(label='Bank ID', choices=[(i, i) for i in list(Access.objects.filter(perid=self._username).values_list('bankid', flat=True).distinct())])
            self.fields['ip_to_accountid'] = forms.ChoiceField(label='Account ID', choices=[(i, i) for i in list(Access.objects.filter(perid=self._username).values_list('accountid', flat=True).distinct())])

    
class AccountDepositForm(forms.Form):
    ip_deposit_amount = forms.IntegerField(min_value=0)
    ip_bankid = forms.ChoiceField(label='Bank ID', choices=[(i, i) for i in list(Access.objects.all().values_list('bankid', flat=True).distinct())])
    ip_accountid = forms.ChoiceField(label='Account ID', choices=[(i, i) for i in list(Access.objects.all().values_list('accountid', flat=True).distinct())])

    def __init__(self, *args, **kwargs):
        self._username = kwargs.pop('username', None)
        super(AccountDepositForm, self).__init__(*args, **kwargs)
        if self._username:
            self.fields['ip_bankid'] = forms.ChoiceField(label='Bank ID', choices=[(i, i) for i in list(Access.objects.filter(perid=self._username).values_list('bankid', flat=True).distinct())])
            self.fields['ip_accountid'] = forms.ChoiceField(label='Account ID', choices=[(i, i) for i in list(Access.objects.filter(perid=self._username).values_list('accountid', flat=True).distinct())])


class AccountWithdrawalForm(forms.Form):
    ip_withdrawal_amount = forms.IntegerField(min_value=0)
    ip_bankid = forms.ChoiceField(label='Bank ID', choices=[(i, i) for i in list(Access.objects.all().values_list('bankid', flat=True).distinct())])
    ip_accountid = forms.ChoiceField(label='Account ID', choices=[(i, i) for i in list(Access.objects.all().values_list('accountid', flat=True).distinct())])

    def __init__(self, *args, **kwargs):
        self._username = kwargs.pop('username', None)
        super(AccountWithdrawalForm, self).__init__(*args, **kwargs)
        if self._username:
            self.fields['ip_bankid'] = forms.ChoiceField(label='Bank ID', choices=[(i, i) for i in list(Access.objects.filter(perid=self._username).values_list('bankid', flat=True).distinct())])
            self.fields['ip_accountid'] = forms.ChoiceField(label='Account ID', choices=[(i, i) for i in list(Access.objects.filter(perid=self._username).values_list('accountid', flat=True).distinct())])


class CreateFeeForm(forms.Form):
    ip_fee_type = forms.CharField(label='Fee Type', max_length=100)
    ip_bankid = forms.ChoiceField(label='Bank ID', choices=[(i, i) for i in list(Access.objects.all().values_list('bankid', flat=True).distinct())])
    ip_accountid = forms.ChoiceField(label='Account ID', choices=[(i, i) for i in list(Access.objects.all().values_list('accountid', flat=True).distinct())])


class ManageOverdraftForm(forms.Form):
    ip_checking_bankid = forms.ChoiceField(label='Checking Bank ID',choices=[(i, i) for i in list(Checking.objects.all().values_list('bankid', flat=True).distinct())])  
    ip_checking_accountid = forms.ChoiceField(label='Checking Account ID', choices=[(i, i) for i in list(Checking.objects.all().values_list('accountid', flat=True).distinct())])
    ip_add_overdraft = forms.BooleanField(label='Adding Overdraft Policy?', required=False)
    ip_savings_bankid = forms.ChoiceField(label='Saving Bank ID',choices=[(i, i) for i in list(Savings.objects.all().values_list('bankid', flat=True).distinct())])  
    ip_savings_accountid = forms.ChoiceField(label='Saving Account ID',choices=[(i, i) for i in list(Savings.objects.all().values_list('accountid', flat=True).distinct())])  


class AddAccountAccessForm(forms.Form):
    ip_accountID = forms.ChoiceField(label='Accessible Accounts', choices=[(i, i) for i in list(BankAccount.objects.all().values_list('accountid', flat=True).distinct())])
    ip_customer = forms.ChoiceField(label='Customer', choices=[(i, i) for i in list(Customer.objects.all().values_list('perid', flat=True).distinct())])
    ip_add_account_access = forms.BooleanField(label='Adding Owner?')


class StartEmployeeForm(forms.Form):
    ip_perID = forms.CharField(label='Person ID', max_length=100)
    ip_taxID = forms.CharField(label='Tax ID', max_length=11)
    ip_firstName = forms.CharField(label='First name', max_length=100)
    ip_lastName = forms.CharField(label='Last name', max_length=100)
    ip_birthdate = forms.DateField(label='Birth Date')
    ip_street = forms.CharField(label='Street', max_length=100)
    ip_city = forms.CharField(label='City', max_length=100)
    ip_state = forms.CharField(label='State', max_length=2)
    ip_zip = forms.CharField(label='Zip', max_length=5)
    ip_dtJoined = forms.DateField(label='Date Joined')
    ip_salary = forms.IntegerField(label='Salary', min_value=0)
    ip_payments = forms.IntegerField(label='Number of Payments', min_value=0)
    ip_earned = forms.IntegerField(label='Earned', min_value=0)
    emp_password = forms.CharField(label='Password', max_length=100)


class HireWorkerForm(forms.Form):
    ip_perid = forms.ChoiceField(label='Person ID', choices=[(i, i) for i in list(Employee.objects.all().values_list('perid', flat=True).distinct())])
    ip_bankid = forms.ChoiceField(label='Bank ID', choices=[(i, i) for i in list(Bank.objects.all().values_list('bankid', flat=True).distinct())])
    ip_salary = forms.IntegerField(label='Salary', min_value=0)
    

class StopEmployeeForm(forms.Form):
    ip_perID = forms.ChoiceField(label='Person ID', choices=[(i, i) for i in list(Employee.objects.all().values_list('perid', flat=True).distinct())])
    
    def __init__(self, *args, **kwargs):
        super(StopEmployeeForm, self).__init__(*args, **kwargs)
        self.fields['ip_perID'] = forms.ChoiceField(label='Person ID', choices=[(i, i) for i in list(Employee.objects.all().values_list('perid', flat=True).distinct())])


class ReplaceManagerForm(forms.Form):
    ip_bankID = forms.ChoiceField(label='Bank', choices=[(i, i) for i in list(Bank.objects.all().values_list('bankid', flat=True).distinct())])
    ip_perID = forms.ChoiceField(label='Employee', choices=[(i, i) for i in list(Employee.objects.all().values_list('perid', flat=True).distinct())])
    ip_salary = forms.IntegerField(label="New Salary", min_value=0)
    
    def __init__(self, *args, **kwargs):
        super(ReplaceManagerForm, self).__init__(*args, **kwargs)
        self.fields['ip_bankID'] = forms.ChoiceField(label='Bank', choices=[(i, i) for i in list(Bank.objects.all().values_list('bankid', flat=True).distinct())])
        self.fields['ip_perID'] = forms.ChoiceField(label='Employee', choices=[(i, i) for i in list(Employee.objects.all().values_list('perid', flat=True).distinct())])


class ManageAccountsAdminForm(forms.Form):
    ip_customer = forms.ChoiceField(label='Customer', choices=[(i, i) for i in list(Customer.objects.all().values_list('perid', flat=True).distinct())])
    ip_account_type = forms.ChoiceField(label='Account Type', choices=[('checking', 'checking'), ('savings', 'savings'), ('market', 'market')])
    ip_bankid = forms.ChoiceField(label='Bank ID', choices=[(i, i) for i in list(Bank.objects.all().values_list('bankid', flat=True).distinct())])
    ip_accountid = forms.CharField(label='Account ID', max_length=100)
    ip_balance = forms.IntegerField(label='Initial Balance')
    ip_interest_rate = forms.IntegerField(label='Interest Rate', required=False)
    ip_dt_deposit = forms.DateField(label='Date Deposit', required=False)
    ip_min_balance = forms.IntegerField(label='Min Balance', required=False)
    ip_num_withdrawals = forms.IntegerField(label='Number of Withdrawals', required=False)
    ip_max_withdrawals = forms.IntegerField(label='Max Withdrawals', required=False, min_value=0)
    ip_dt_share_start = forms.DateField(label='Date Share Start')


class ManageAccountsCustomerForm(forms.Form):
    ip_customer = forms.ChoiceField(label='Customer', choices=[(i, i) for i in list(Customer.objects.all().values_list('perid', flat=True).distinct())])
    ip_bankid = forms.ChoiceField(label='Bank ID')
    ip_accountid = forms.ChoiceField(label='Account ID')
    # ip_dt_share_start = forms.DateField(label='Date Share Start', required=False)
    ip_add_owner = forms.BooleanField(label='Adding Owner?', required=False)

    
    def __init__(self, *args, **kwargs):
        self._username = kwargs.pop('username', None)
        super(ManageAccountsCustomerForm, self).__init__(*args, **kwargs)
        if self._username:
            self.fields['ip_accountid'] = forms.ChoiceField(label='Account ID', choices=[(i, i) for i in list(Access.objects.filter(perid=self._username).values_list('accountid', flat=True).distinct())])
            self.fields['ip_bankid'] = forms.ChoiceField(label='Bank ID', choices=[(i, i) for i in list(Access.objects.filter(perid=self._username).values_list('bankid', flat=True).distinct())])


class RemoveAccountsAccessForm(forms.Form):
    ip_customer = forms.ChoiceField(label='Customer', choices=[(i, i) for i in list(Customer.objects.all().values_list('perid', flat=True).distinct())])
    ip_bankid = forms.ChoiceField(label='Bank ID', choices=[(i, i) for i in list(Bank.objects.all().values_list('bankid', flat=True).distinct())])
    ip_accountid = forms.ChoiceField(label='Account ID', choices=[(i, i) for i in list(BankAccount.objects.all().values_list('accountid', flat=True).distinct())])
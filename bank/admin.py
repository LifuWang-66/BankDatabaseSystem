from django.contrib import admin

from .models import Access, Bank, BankAccount, BankUser, Checking, Corporation, Customer, CustomerContacts, Employee, InterestBearing, InterestBearingFees, Market, Person, Savings, SystemAdmin, Workfor
# Register your models here.
admin.site.register(Access)
admin.site.register(Bank)
admin.site.register(BankAccount)
admin.site.register(BankUser)
admin.site.register(Checking)
admin.site.register(Corporation)
admin.site.register(Customer)
admin.site.register(CustomerContacts)
admin.site.register(Employee)
admin.site.register(InterestBearing)
admin.site.register(InterestBearingFees)
admin.site.register(Market)
admin.site.register(Person)
admin.site.register(Savings)
admin.site.register(SystemAdmin)
admin.site.register(Workfor)
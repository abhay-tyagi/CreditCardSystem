# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from Website.models import Account, Bank, CreditCard, Transaction, FundTransfer

# Register your models here.

admin.site.register(Account)
admin.site.register(Bank)
admin.site.register(CreditCard)

class TransactionAdmin(admin.ModelAdmin):
    readonly_fields = ('time',)
admin.site.register(Transaction, TransactionAdmin)

class FundTransferAdmin(admin.ModelAdmin):
    readonly_fields = ('time',)
admin.site.register(FundTransfer, FundTransferAdmin)
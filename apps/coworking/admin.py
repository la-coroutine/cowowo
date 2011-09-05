"""
Django Admin for member stuff
"""
from django.contrib import admin

from .models import Transaction, Service, Pack, PackServiceAmount

class TransactionAdmin(admin.ModelAdmin):
    model = Transaction
    list_display = ('date', 'card', 'kind', 'amount', 'label')

class ServiceAdmin(admin.ModelAdmin):
    model = Service
    list_display = ('label', 'cost')

class PackServiceAmountInline(admin.TabularInline):
    model = PackServiceAmount

class PackAdmin(admin.ModelAdmin):
    inlines = [PackServiceAmountInline]

    model = Pack
    list_display = ('label', 'cost')


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Pack, PackAdmin)




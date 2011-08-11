"""
Django Admin for member stuff
"""
from django.contrib import admin

from .models import MembershipCard, Transaction, Service

class MembershipCardAdmin(admin.ModelAdmin):
    model = MembershipCard
    list_display = ('user', 'uuid', 'remaining_units')

class TransactionAdmin(admin.ModelAdmin):
    model = Transaction
    list_display = ('date', 'card', 'kind', 'amount', 'label')

class ServiceAdmin(admin.ModelAdmin):
    model = Service
    list_display = ('label', 'cost')


admin.site.register(MembershipCard, MembershipCardAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Service, ServiceAdmin)




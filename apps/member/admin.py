"""
Django Admin for member stuff
"""
from django.contrib import admin

from .models import MembershipCard

from .models import ServiceUnits

class ServiceUnitsInline(admin.TabularInline):
    model = ServiceUnits

class MembershipCardAdmin(admin.ModelAdmin):
    inlines = [ServiceUnitsInline]
    model = MembershipCard
    list_display = ('user', 'uuid', 'credit')


admin.site.register(MembershipCard, MembershipCardAdmin)




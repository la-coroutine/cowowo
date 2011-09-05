from django import forms

from .models import Transaction, Service, ServiceConsumption, Pack

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('amount', )

    amount = forms.IntegerField(widget=forms.HiddenInput())


class PackForm(forms.ModelForm):
    class Meta:
        model = Pack
        fields = ('id',)

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service


class ServiceConsumptionForm(forms.ModelForm):
    class Meta:
        model = ServiceConsumption
        fields = ('service', )






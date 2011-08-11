from django import forms

from .models import Transaction, Service, ServiceConsumption

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('amount', )

    amount = forms.IntegerField(widget=forms.HiddenInput())


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service


class ServiceConsumptionForm(forms.ModelForm):
    class Meta:
        model = ServiceConsumption
        fields = ('service', )






#-- encoding: utf-8 --

from django.views.generic.list_detail import object_detail

from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.core.urlresolvers import reverse

from django.contrib.auth import login
from django.contrib.auth.models import User

from django.http import HttpResponseBadRequest

from .models import MembershipCard, CoroutineProfile, Transaction
from .forms import TransactionForm, ServiceConsumptionForm


def login_by_uuid(request, card_uuid):
    try:
        membership_card = MembershipCard.objects.get(uuid=card_uuid)
    except MembershipCard.DoesNotExist:
        redirect('/')

    user = membership_card.user.user

    user.backend = 'django.contrib.auth.backends.ModelBackend'
    if  user.is_active:
        login(request, user)

    return redirect('userena_profile_detail', user.username)


def buy_credit(request):
    member_card = get_object_or_404(MembershipCard, user=request.user.get_profile())

    if request.method == 'GET':
        transaction_form = TransactionForm(request.GET)
        amount = request.GET.get('amount', None)
        if not amount:
            return render_to_response(template_name='member/buy_choose.html')
        else:
            return render_to_response(template_name='member/buy_confirm.html',
                                      dictionary={'amount': amount,
                                                  'transaction_form': transaction_form},
                                      context_instance=RequestContext(request)
                                      )

    elif request.method == 'POST':
        transaction_form = TransactionForm(request.POST)
        if transaction_form.is_valid():
            # Create the transaction
            transaction = transaction_form.save(commit=False)
            transaction.kind = 'CREDIT'
            transaction.label = "Acheté à crédit par l'interface web"
            transaction.card = member_card
            transaction.save()

            # Add the amount to the card
            member_card.remaining_units += transaction.amount
            member_card.save()

            return redirect(member_card.user)
        else:
            return HttpResponseBadRequest()
    
# Login req
def service_list(request):
    old_transactions = Transaction.objects.filter(card__user__user=request.user)

    service_cons_form = ServiceConsumptionForm(request.GET or None)

    return render_to_response(template_name='member/service_list.html',
                              dictionary={'service_cons_form': service_cons_form,
                                          'old_transactions': old_transactions},
                              context_instance=RequestContext(request)
                              )


# login required
# POST required
def service_buy(request):
    membership_card = request.user.get_profile().membership_card

    service_cons_form = ServiceConsumptionForm(request.POST or None)

    if service_cons_form.is_valid():
        # Initiate service consumption
        service_cons = service_cons_form.save(commit=False)
        service_cons.card = membership_card
        
        # Check if the member has enought credit
        if service_cons.service.cost <= membership_card.remaining_units:
            transaction = Transaction.objects.create(kind='DEBIT',
                                                     label='%s' % service_cons.service,
                                                     card=membership_card,
                                                     amount=service_cons.service.cost
                                                     )
            service_cons.transaction = transaction

            # Debit the member
            membership_card.remaining_units -= service_cons.service.cost
        else:
            return render_to_response(template_name='member/service_no_credit.html',
                                      context_instance=RequestContext(request))

        membership_card.save()
        service_cons.save()

        # add a notification

        return redirect(request.user.get_profile())


            
                
                


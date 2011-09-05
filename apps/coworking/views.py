#-- encoding: utf-8 --

from django.views.generic.list_detail import object_detail

from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.core.urlresolvers import reverse

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.http import HttpResponseBadRequest

from apps.member.models import MembershipCard, ServiceUnits

from .models import Pack, Transaction
from .forms import TransactionForm, PackForm, ServiceConsumptionForm


@login_required
def buy_credit(request):
    member_card = get_object_or_404(MembershipCard, user=request.user.get_profile())

    if request.method == 'GET':
        transaction_form = TransactionForm(request.GET)
        amount = request.GET.get('amount', None)
        if not amount:
            return render_to_response(template_name='coworking/buy_choose.html')
        else:
            return render_to_response(template_name='coworking/buy_confirm.html',
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
            transaction.label = u"Acheté à crédit par l'interface web"
            transaction.card = member_card
            transaction.save()

            # Add the amount to the card
            member_card.credit += transaction.amount
            member_card.save()

            return redirect(member_card.user)
        else:
            return HttpResponseBadRequest()


    
@login_required
def service_list(request):
    old_transactions = Transaction.objects.filter(card__user__user=request.user)

    service_cons_form = ServiceConsumptionForm(request.GET or None)

    return render_to_response(template_name='coworking/service_list.html',
                              dictionary={'service_cons_form': service_cons_form,
                                          'old_transactions': old_transactions},
                              context_instance=RequestContext(request)
                              )


# POST required
@login_required
def service_buy(request):
    membership_card = request.user.get_profile().membership_card

    service_cons_form = ServiceConsumptionForm(request.POST or None)

    if service_cons_form.is_valid():
        # Initiate service consumption
        service_cons = service_cons_form.save(commit=False)
        service_cons.card = membership_card
        
        # Check if the member has enought credit
        if service_cons.service.cost <= membership_card.credit:
            transaction = Transaction.objects.create(kind='DEBIT',
                                                     label='%s' % service_cons.service,
                                                     card=membership_card,
                                                     amount=service_cons.service.cost
                                                     )
            service_cons.transaction = transaction

            # Debit the member
            membership_card.credit -= service_cons.service.cost
        else:
            return render_to_response(template_name='coworking/service_no_credit.html',
                                      context_instance=RequestContext(request))

        membership_card.save()
        service_cons.save()

        # add a notification

        return redirect(request.user.get_profile())


# require post
@login_required
def buy_pack(request, pack_id=None):
    if pack_id:
        pack = get_object_or_404(Pack, id=pack_id)

    membership_card = get_object_or_404(MembershipCard, user=request.user.get_profile())

    if request.method == 'GET':
        if not pack_id:
            pack_list = Pack.objects.all()
            return render_to_response(template_name='coworking/pack_buy_choose.html',
                                      dictionary={'pack_list': pack_list},
                                      context_instance=RequestContext(request)
                                      )
        else:
            pack_form = PackForm(request.GET, instance=pack)
            return render_to_response(template_name='coworking/pack_buy_confirm.html',
                                      dictionary={'pack': pack,
                                                  'pack_form': pack_form},
                                      context_instance=RequestContext(request)
                                      )

    elif request.method == 'POST':
        pack_form = PackForm(request.POST, instance=pack)

        if pack_form.is_valid():
            if pack.cost <= membership_card.credit:
                # Create the transaction
                transaction = Transaction.objects.create(kind='DEBIT',
                                                         amount=pack.cost,
                                                         label=u"Achat du pack '%s'" % pack,
                                                         card=membership_card)

                # Credit units
                for service_amount in pack.service_amounts.all():
                    print service_amount.service
                    service_units, created = ServiceUnits.objects.get_or_create(card=membership_card,
                                                                                service=service_amount.service)
                    service_units.amount += service_amount.amount
                    service_units.save()
                    
                # Draw the amount from the card
                membership_card.credit -= transaction.amount
                
                membership_card.save()

                return redirect(membership_card.user)
            else:
                return render_to_response(template_name='coworking/service_no_credit.html',
                                          context_instance=RequestContext(request))
        else:
            return HttpResponseBadRequest()


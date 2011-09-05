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

from .models import MembershipCard, CoroutineProfile

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




            
                
                


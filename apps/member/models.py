#-- encoding: utf-8 --

from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

from django_extensions.db.fields import UUIDField
from userena.models import UserenaLanguageBaseProfile
from userena.models import PROFILE_PERMISSIONS

from apps.coworking.models import Service, ServiceConsumption

class CoroutineProfile(UserenaLanguageBaseProfile):
    """
    Userena Profile with language switch
    """
    class Meta:
        permissions = PROFILE_PERMISSIONS


    GENDER_TYPE = (
       ('M', _('male')),
       ('F', _('female'))
    )
    gender = models.CharField(max_length=1, choices=GENDER_TYPE, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    about = models.TextField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    website = models.URLField(verbose_name=_('website'), verify_exists=True, max_length=200, blank=True)
    linkedin = models.URLField(verbose_name=_('linkedin'), verify_exists=True, max_length=200, blank=True)
    twitter = models.URLField(verbose_name=_('twitter'), verify_exists=True, max_length=200, blank=True)
    facebook = models.URLField(verbose_name=_('facebook'), verify_exists=True, max_length=200, blank=True)

    user = models.ForeignKey(User)

    @models.permalink
    def get_absolute_url(self):
        return ('userena_profile_detail', (), {'username': self.user.username})


class ServiceUnits(models.Model):
    """
    Available Units for a given service
    """
    card = models.ForeignKey('member.MembershipCard', related_name='remaining_units')
    service = models.ForeignKey(Service, related_name='user_units')
    amount = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return "%s - %s" % (self.service.label, self.amount)

class MembershipCard(models.Model):
    uuid = UUIDField(unique=True, db_index=True, auto=True, editable=True)

    user = models.OneToOneField(CoroutineProfile, related_name='membership_card')

    credit = models.PositiveIntegerField(default=0)
    units = models.ManyToManyField(Service, through=ServiceUnits)

    consumptions = models.ManyToManyField(Service, through=ServiceConsumption,
                                          related_name='membership_card')
    
    # Expiration

    def __unicode__(self):
        return u"Membership card of %s" % self.user.user





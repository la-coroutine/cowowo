#-- encoding: utf-8 --

from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

from django_extensions.db.fields import UUIDField
from userena.models import UserenaLanguageBaseProfile
from userena.models import PROFILE_PERMISSIONS

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


class MembershipCard(models.Model):
    uuid = UUIDField(unique=True, db_index=True, auto=True, editable=True)

    user = models.OneToOneField(CoroutineProfile, related_name='membership_card')

    remaining_units = models.PositiveIntegerField(default=0)

    consumptions = models.ManyToManyField('Service', through='ServiceConsumption')
    
    # Expiration

    def __unicode__(self):
        return u"Membership card of %s" % self.user.user


### Transactions
class Transaction(models.Model):
    TRANSACTION_KINDS = (
        ('CREDIT', 'Crédit'),
        ('DEBIT', 'Débit')
        )

    amount = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    label = models.CharField(max_length=200, null=True, blank=True)
    kind = models.CharField(max_length=6, choices=TRANSACTION_KINDS)
    card = models.ForeignKey(MembershipCard, related_name='transactions')

### Services
class Service(models.Model):
    """
    An available service
    """
    label = models.CharField(max_length=200)
    cost = models.PositiveIntegerField()

    def __unicode__(self):
        return u"%s (%s €)" % (self.label, self.cost)

class ServiceConsumption(models.Model):
    """
    When a member buys a service
    """
    card = models.ForeignKey(MembershipCard, related_name='services')
    transaction = models.OneToOneField(Transaction)    
    service = models.ForeignKey(Service, related_name='consumptoins')





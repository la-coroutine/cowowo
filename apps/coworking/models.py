#-- encoding: utf-8 --

from django.db import models

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
    card = models.ForeignKey('member.MembershipCard', related_name='transactions')

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
    card = models.ForeignKey('member.MembershipCard', related_name='services')
    transaction = models.OneToOneField(Transaction)    
    service = models.ForeignKey(Service, related_name='consumptions')


class PackServiceAmount(models.Model):
    """
    A service and its associated quantity
    """
    pack = models.ForeignKey('Pack', related_name='service_amounts')
    service = models.ForeignKey(Service)
    amount = models.PositiveIntegerField()

class Pack(models.Model):
    """
    A pack is a set of discounted services that preloads your card
    """
    label = models.CharField(max_length=200)
    cost = models.PositiveIntegerField()

    services = models.ManyToManyField(Service, through=PackServiceAmount)

    def __unicode__(self):
        return u"Pack %s" % self.label




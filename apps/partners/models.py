from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# models
from apps.markets.models import PayTypes, FiatCurrency


class Partner(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='partner_profile'
    )
    token = models.CharField(blank=True, max_length=255)
    google_doc_id = models.CharField(
        help_text='google spreadsheet document id',
        blank=True,
        max_length=100,
    )
    google_sheet_name = models.CharField(
        help_text='google spreadsheet table name',
        default='Sheet1',
        max_length=50,
    )

    # "accept fiat"
    accept_fiats = models.ManyToManyField(FiatCurrency, blank=True)

    # "accept pay types" - array of strings -- select in admin, of pay types what we received from binance by partner "accept fiat"
    accept_pay_types = models.ManyToManyField(PayTypes, blank=True)

    class Meta:
        db_table = 'auth_partner'

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)  # signal used to create a object related to user instance
def create_user_partner(sender, instance, created, **kwargs):
    if created:
        Partner.objects.create(user=instance)


@receiver(post_save, sender=User)  # signal used to save a object related to user instance
def save_user_partner(sender, instance, **kwargs):
    instance.partner_profile.save()

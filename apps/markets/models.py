from django.db import models
from django_cryptography.fields import encrypt

class Market(models.Model):
    name = models.CharField(
        max_length=128,
        help_text='Binance, Bybit, WhiteBit,...'
    )
    description = models.TextField()

    class Meta:
        db_table = 'market'
        ordering = ["name"]

    def __str__(self):
        return self.name

class MarketAccount(models.Model):
    name = models.CharField(
        max_length=200,
        help_text='Binance, Bybit, WhiteBit,...'
    )
    description = models.TextField()
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    api_key = encrypt(models.CharField(blank=True, null=True, max_length=300))
    secret_key = encrypt(models.CharField(blank=True, null=True, max_length=300))

    class Meta:
        db_table = 'market_account'
        ordering = ["name"]

    def __str__(self):
        return self.name


class PayTypes(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=128,
        help_text='Binance order pay type. Like Payeer, Bank of America, ...'
    )

    class Meta:
        db_table = 'pay_types'
        ordering = ["name"]

    def __str__(self):
        return self.name

class FiatCurrency(models.Model):
    name = models.CharField(
        max_length=128,
        help_text='UAH, AUD, CHF, ...'
    )

    class Meta:
        db_table = 'fiat_currency'
        ordering = ["name"]

    def __str__(self):
        return self.name
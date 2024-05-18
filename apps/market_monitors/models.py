from django.db import models

from apps.market_monitors.const import BUY_TRADE_TYPE, SELL_TRADE_TYPE

# models
from apps.markets.models import FiatCurrency, Market
from apps.partners.models import PayTypes


class Radar(models.Model):
    name = models.CharField(
        max_length=128,
        help_text='Binance, Bybit, WhiteBit,...'
    )
    description = models.TextField(help_text="Description")
    doc_id = models.CharField(
        max_length=50,
        help_text='google spreadsheet doc id'
    )
    sheet_name = models.CharField(
        max_length=50,
        help_text='google spreadsheet table name'
    )
    first_row = models.IntegerField(
        default=2,
        help_text='1, 2, 3,...'
    )
    fiat = models.ForeignKey(FiatCurrency, on_delete=models.SET_NULL, null=True)
    pay_type = models.ForeignKey(PayTypes, on_delete=models.SET_NULL, null=True)
    market = models.ForeignKey(Market, on_delete=models.SET_NULL, null=True)
    trade_type = models.CharField(max_length=4, choices=[(BUY_TRADE_TYPE, BUY_TRADE_TYPE), (SELL_TRADE_TYPE, SELL_TRADE_TYPE)], default=SELL_TRADE_TYPE)

    class Meta:
        db_table_comment = 'reports system about p2p orders on the market'

    def __str__(self):
        return self.name
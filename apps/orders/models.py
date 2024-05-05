from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from apps.partners.models import Partner
from common.util.is_json import is_json


class Order(models.Model):
    partner = models.ForeignKey(
        Partner,
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField()
    orderId = models.CharField(max_length=255)
    card = models.CharField(null=False, max_length=16)
    payoutAmount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    status = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ]
    )

    rowNum = models.PositiveIntegerField(
        default=None,
        blank=True,
        null=True
    )
    screenshot = models.CharField(
        max_length=255,
        blank=True,
        default='',
        # null=True # nullable value for CharField is not recommended in doc - https://stackoverflow.com/a/44272461
    )
    compensation = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
    )
    rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
    )

    # partner callback api request
    callbackUrl = models.URLField()
    callbackMethod = models.CharField(max_length=8)
    callbackHeaders = models.TextField()
    callbackBody = models.TextField()

    def clean(self):
        if self.callbackHeaders and is_json(self.callbackHeaders) is False:
            raise ValidationError("callback headers contains not valid JSON string.")
        elif self.callbackBody and is_json(self.callbackBody) is False:
            raise ValidationError("callback body contains not valid JSON string.")

    def __str(self):
        return self.orderId

    class Meta:
        db_table_comment = 'income orders from partners'

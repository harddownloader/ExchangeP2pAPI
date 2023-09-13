from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class OrderModel(models.Model):
    orderId = models.CharField(max_length=255)
    date = models.DateTimeField(blank=False)
    card = models.CharField(null=False, max_length=16)
    payoutAmount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    status = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            # MaxValueValidator(5)
        ]
    )

    rowNum = models.PositiveIntegerField(
        default=None,
        blank=True,
        null=True
    )
    screenshot = models.CharField(
        max_length=255,
        default=None,
        blank=True,
        null=True
    )

    def __str(self):
        return self.orderId

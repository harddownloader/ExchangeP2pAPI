from django.core.validators import MinValueValidator
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import Order


class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    orderId = serializers.CharField(max_length=255)
    date = serializers.DateTimeField()
    card = serializers.CharField(max_length=16)
    payoutAmount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    status = serializers.IntegerField(
        validators=[
            MinValueValidator(0),
            # MaxValueValidator(5)
        ],
        required=False
    )
    rowNum = serializers.IntegerField(required=False)
    screenshot = serializers.CharField(max_length=255, required=False, default='')

    def create(self, validated_data):
        return Order.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.orderId

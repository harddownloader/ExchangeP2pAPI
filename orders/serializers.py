from django.core.validators import MinValueValidator
from rest_framework import serializers
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

    callbackUrl = serializers.URLField()
    callbackMethod = serializers.CharField(max_length=8)
    callbackHeaders = serializers.JSONField()  # serializers.CharField()
    callbackBody = serializers.CharField()

    def validate(self, attrs):
        instance = Order(**attrs)
        instance.clean()
        return attrs

    def create(self, validated_data):
        return Order.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.orderId

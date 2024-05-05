from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ['partner']

class P2PMarketOrdersSerializer(serializers.Serializer):
    tradeType = serializers.ChoiceField(choices=["BUY", "SELL"])
    payType = serializers.ChoiceField(choices=["Monobank", "PrivatBank"])

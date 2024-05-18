from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ['partner']

class P2PMarketOrdersSerializer(serializers.Serializer):
    market_monitor_id = serializers.IntegerField(min_value=1)

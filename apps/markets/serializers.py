from rest_framework import serializers

# models
from apps.markets.models import Market, MarketAccount, PayTypes, FiatCurrency


class MarketsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = '__all__'


class MarketAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketAccount
        fields = '__all__'


class PayTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayTypes
        fields = '__all__'


class FiatCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = FiatCurrency
        fields = '__all__'
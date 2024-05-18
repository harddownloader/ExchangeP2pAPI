from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from apps.markets.models import Market, MarketAccount, PayTypes, FiatCurrency
from apps.markets.serializers import MarketsSerializer, MarketAccountSerializer, PayTypesSerializer, \
    FiatCurrencySerializer


class MarketsCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAdminUser,)
    queryset = Market.objects.all()
    serializer_class = MarketsSerializer

class MarketsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser,)
    queryset = Market.objects.all()
    serializer_class = MarketsSerializer


class MarketAccountCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAdminUser,)
    queryset = MarketAccount.objects.all()
    serializer_class = MarketAccountSerializer

class MarketAccountRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser,)
    queryset = MarketAccount.objects.all()
    serializer_class = MarketAccountSerializer

class PayTypesCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAdminUser,)
    queryset = PayTypes.objects.all()
    serializer_class = PayTypesSerializer

class PayTypesAccountRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser,)
    queryset = PayTypes.objects.all()
    serializer_class = PayTypesSerializer

class FiatCurrencyCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAdminUser,)
    queryset = FiatCurrency.objects.all()
    serializer_class = FiatCurrencySerializer

class FiatCurrencyAccountRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser,)
    queryset = FiatCurrency.objects.all()
    serializer_class = FiatCurrencySerializer


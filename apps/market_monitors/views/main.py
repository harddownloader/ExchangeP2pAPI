from rest_framework.permissions import IsAdminUser
from rest_framework import generics
from apps.market_monitors.models import Radar
from apps.market_monitors.serializers import MarketMonitorsSerializer

class MarketMonitorCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAdminUser,)
    queryset = Radar.objects.all()
    serializer_class = MarketMonitorsSerializer

class MarketMonitorsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser,)
    queryset = Radar.objects.all()
    serializer_class = MarketMonitorsSerializer

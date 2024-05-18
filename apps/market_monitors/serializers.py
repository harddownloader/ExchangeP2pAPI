from rest_framework import serializers

from apps.market_monitors.models import Radar


class MarketMonitorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Radar
        fields = '__all__'

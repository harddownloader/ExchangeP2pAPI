from rest_framework import serializers
from .models import Partner


class PartnerSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255, required=False)
    google_doc_id = serializers.CharField(max_length=100, required=False)
    # username = serializers.CharField(max_length=255, required=False)

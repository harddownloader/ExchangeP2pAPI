from rest_framework import serializers
from .models import Partner
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_active',
        )


class PartnerSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255, required=False)
    google_doc_id = serializers.CharField(max_length=100, required=False)
    google_sheet_name = serializers.CharField(max_length=50, required=False)
    user = UserSerializer()

    class Meta:
        model = Partner
        fields = ('token', 'google_doc_id', 'google_sheet_name', 'user')

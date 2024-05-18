from django.http import JsonResponse
from rest_framework.permissions import IsAdminUser
from rest_framework import generics
from .models import Partner
from .serializers import PartnerSerializer


class PartnersAPIList(generics.ListAPIView):
    permission_classes = (IsAdminUser, )
    queryset = Partner.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = PartnerSerializer(queryset, many=True)
        return JsonResponse(
            list(serializer.data),
            safe=False
        )

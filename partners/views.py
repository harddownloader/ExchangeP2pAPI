from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework import generics, viewsets, mixins
from .models import Partner
from .serializers import PartnerSerializer
from django.contrib.auth import get_user_model


# Create your views here.
class PartnersAPIList(generics.ListAPIView):
    # queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    permission_classes = (IsAuthenticated, )
    User = get_user_model()
    queryset = User.objects.all()


def get_users_as_json(request):
    col = ['username', 'first_name', 'last_name', 'partner__token', 'partner__google_doc_id']

    User = get_user_model()
    all_users = User.objects.all().values(*col)
    user_list = list(all_users)

    return JsonResponse(user_list, safe=False)

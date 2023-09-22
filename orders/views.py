import sys
import os
from datetime import datetime
from dateutil import parser
import logging

from django.forms import model_to_dict
from rest_framework import generics, viewsets, mixins, status
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework import filters

from common.spreadsheets import insert_new_row

from .models import Order
from .serializers import OrderSerializer
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly

from partners.models import Partner

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# get all / create one
class OrdersAPIList(generics.ListCreateAPIView):
    model = Order

    logger.info("Houston, we have a %s", "interesting problem", exc_info=1)
    # queryset = Order.objects.all()
    # serializer_class = OrderSerializer
    # permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        logger.info('get_serializer_class', exc_info=1)
        if self.request.method == 'POST':
            return OrderSerializer
        return OrderSerializer

    def get_queryset(self):
        logger.info('get_queryset', exc_info=1)
        partner = Partner.objects.filter(user_id=self.request.user.id)[0]

        order_id = self.request.query_params.get('order_id')
        if order_id is not None:
            return Order.objects.filter(partner=partner, orderId=order_id)

        return Order.objects.filter(partner=partner)

    def create(self, request, *args, **kwargs):
        logger.info('create', exc_info=1)
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        partner = Partner.objects.get(user_id=request.user.id)

        if not partner.google_doc_id:
            return Response(
                'partner.google_doc_id not found',
                status=status.HTTP_400_BAD_REQUEST
            )

        order = Order.objects.create(
            partner=partner,
            date=serializer.data['date'],
            orderId=serializer.data['orderId'],
            card=serializer.data['card'],
            payoutAmount=serializer.data['payoutAmount']
        )
        date_format = '%Y-%m-%d %H:%M:%S'
        date_obj = parser.parse(serializer.data['date'], ignoretz=True)
        date_str = date_obj.strftime(date_format)

        insert_new_row(
            new_order={
                "date": date_str,
                "orderId": serializer.data['orderId'],
                "card": serializer.data['card'],
                "payoutAmount": serializer.data['payoutAmount'],
                # "status": 0, # status is text, and it will set automatically by spreadsheets
            },
            spreadsheet_id=partner.google_doc_id
        )

        result = OrderSerializer(order)

        return Response(result.data, status=status.HTTP_201_CREATED)


# update one
class OrderAPIUpdate(generics.RetrieveUpdateAPIView):
    logger.info('OrderAPIUpdate', exc_info=1)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAdminUser, )


# delete one
class OrderAPIDestroy(generics.RetrieveDestroyAPIView):
    logger.info('OrderAPIDestroy', exc_info=1)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAdminOrReadOnly, )


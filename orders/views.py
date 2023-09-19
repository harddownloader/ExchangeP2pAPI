from datetime import datetime

from django.forms import model_to_dict
from rest_framework import generics, viewsets, mixins
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .models import Order
from .serializers import OrderSerializer
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly

# class OrdersAPIView(APIView):
#     def get(self, request):
#         orders = OrderModel.objects.all()
#         serializer = OrderSerializer(orders, many=True)
#         return JsonResponse(serializer.data, safe=False)

#     def post(self, request):
#         serializer = OrderSerializer(data=request.data)
#         # serializer.is_valid(raise_exception=True)

#         # deadline = datetime.strptime("05-22-2017T12:30:01", "%m-%d-%Y %H:%M")
#         # deadline = datetime.fromisoformat(request.data['date'])

#         # order_new = OrderModel.objects.create(
#         #     orderId=serialized.validated_data['orderId'],
#         #     date=serialized.validated_data['date'],
#         #     card=serialized.validated_data['card'],
#         #     payoutAmount=serialized.validated_data['payoutAmount'],
#         #     # rowNum=request.data['rowNum'],
#         #     # screenshot=request.data['screenshot']
#         # )
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)

# get all / create one
class OrdersAPIList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, )


# update one
class OrderAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, )

# delete one
class OrderAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAdminOrReadOnly, )


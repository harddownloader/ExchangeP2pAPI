import logging
from rest_framework import generics
from rest_framework.permissions import IsAdminUser


from apps.orders.models import Order
from apps.orders.serializers import OrderSerializer


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# delete one
class OrderAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAdminUser, )

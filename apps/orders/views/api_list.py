from dateutil import parser
import logging

from sentry_sdk import capture_message

from rest_framework import generics, status
from rest_framework.response import Response

# common
from common.spreadsheets import add_order_into_table
from common.exceptions import INSERT_ORDER_INTO_SPREADSHEET, CustomErrors

from apps.orders.models import Order
from apps.orders.serializers import OrderSerializer

from apps.partners.models import Partner

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# get all / create one
class OrdersAPIList(generics.ListCreateAPIView):
    model = Order

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
        logger.info('order create', exc_info=1)
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        partner = Partner.objects.get(user_id=request.user.id)

        if not partner or not partner.google_doc_id:
            return Response(
                'partner.google_doc_id not found',
                status=status.HTTP_400_BAD_REQUEST
            )

        order = Order.objects.create(
            partner=partner,
            date=serializer.data['date'],
            orderId=serializer.data['orderId'],
            card=serializer.data['card'],
            payoutAmount=serializer.data['payoutAmount'],

            # callback request
            callbackUrl=serializer.data['callbackUrl'],
            callbackMethod=serializer.data['callbackMethod'],
            callbackHeaders=serializer.data['callbackHeaders'],
            callbackBody=serializer.data['callbackBody'],
        )
        date_format = '%Y-%m-%d %H:%M:%S'
        date_obj = parser.parse(serializer.data['date'], ignoretz=True)
        date_str = date_obj.strftime(date_format)

        try:
            add_order_into_table(
                new_order={
                    "date": date_str,
                    "orderId": serializer.data['orderId'],
                    "card": serializer.data['card'],
                    "payoutAmount": serializer.data['payoutAmount'],
                    # "status": 0, # status is text, and it will set automatically by spreadsheets
                },
                spreadsheet_id=partner.google_doc_id,
                sheet_name=partner.google_sheet_name
            )
        except:
            capture_message("Something went wrong with inserting new order into the google spreadsheet")
            return Response(
                CustomErrors(INSERT_ORDER_INTO_SPREADSHEET).generate_response(),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        result = OrderSerializer(order)

        return Response(result.data, status=status.HTTP_201_CREATED)

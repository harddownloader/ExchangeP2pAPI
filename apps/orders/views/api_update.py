import os
import json
import pprint

import requests
import base64
import logging
from django.conf import settings

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from common.decimal_encoder import DecimalEncoder
from apps.orders.models import Order
from apps.orders.serializers import OrderSerializer


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_callback(
        callback_url,
        callback_method,
        callback_headers,
        callback_body
):
    pprint.pprint({
        'callback_body': callback_body,
        'callback_body type': type(callback_body),
    })
    public_key_path = os.path.join(settings.BASE_DIR, 'public_key.pem')
    private_key_path = os.path.join(settings.BASE_DIR, 'private_key.pem')

    with open(public_key_path, 'rb') as key_file:
        public_key_pem = key_file.read()

    with open(private_key_path, 'rb') as key_file:
        private_key_pem = key_file.read()

    public_key = serialization.load_pem_public_key(public_key_pem, backend=default_backend())
    private_key = serialization.load_pem_private_key(
        private_key_pem,
        password=None,
        backend=default_backend()
    )

    data_bytes = json.dumps({
        'date': callback_body['date'],
        'orderId': callback_body['orderId'],
        'card': callback_body['card'],
        'payoutAmount': callback_body['payoutAmount'],
        'screenshot': callback_body['screenshot'],
        'compensation': callback_body['compensation']
    }, cls=DecimalEncoder).encode('utf-8')

    encrypted_data = public_key.encrypt(
        data_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # convert to string(base64)
    received_encrypted_data_base64 = base64.b64encode(encrypted_data).decode('utf-8')

    body_content = {
        'data': received_encrypted_data_base64
    }
    headers_content = json.loads(callback_headers)

    if callback_method == 'GET':
        requests.get(
            url=callback_url,
            data=body_content,
            headers=headers_content
        )
    elif callback_method == 'POST':
        requests.post(
            url=callback_url,
            data=body_content,
            headers=headers_content
        )
    elif callback_method == 'PUT':
        requests.put(
            url=callback_url,
            data=body_content,
            headers=headers_content
        )
    elif callback_method == 'PATCH':
        requests.patch(
            url=callback_url,
            data=body_content,
            headers=headers_content
        )
    elif callback_method == 'DELETE':
        requests.delete(
            url=callback_url,
            data=body_content,
            headers=headers_content
        )


# update one
class OrderAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAdminUser, )

    def patch(self, request, *args, **kwargs):
        pprint.pprint({'status': request.data['status']})
        if request.data['status'] and request.data['status'] == 5:
            instance = self.get_object()
            pprint.pprint({
                'title': 'send request',
                'callbackUrl': instance.callbackUrl,
                'callbackMethod': instance.callbackMethod,
                'callbackHeaders': instance.callbackHeaders,
                'callbackBody': instance.callbackBody,
                'order date': instance.date,
                'order date type': type(instance.date),
            })

        date_format = '%Y-%m-%d %H:%M:%S'
        date_str = instance.date.strftime(date_format)

        send_callback(
            callback_url=instance.callbackUrl,
            callback_method=instance.callbackMethod,
            callback_headers=instance.callbackHeaders,
            callback_body={
                **json.loads(instance.callbackBody),
                'date': date_str,
                'orderId': instance.orderId,
                'card': instance.card,
                'payoutAmount': instance.payoutAmount,
                'screenshot': instance.screenshot,
                'compensation': instance.compensation
            },
        )

        return super().patch(request, *kwargs, *args)

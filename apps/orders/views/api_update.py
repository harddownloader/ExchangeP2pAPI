import json
import pprint

import requests
import base64
import logging

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from common.decimal_encoder import DecimalEncoder
from common.const import PUBLIC_KEY, PRIVATE_KEY

from apps.orders.models import Order
from apps.orders.serializers import OrderSerializer


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_callback(
        callback_url,
        callback_method,
        callback_headers,
        data_bytes,
):
    public_key_pem = bytes(PUBLIC_KEY, 'utf-8')

    public_key = serialization.load_pem_public_key(
        public_key_pem,
        backend=default_backend()
    )
    private_key_pem = PRIVATE_KEY.encode('utf-8')

    private_key = serialization.load_pem_private_key(
        private_key_pem,
        password=None,
        backend=default_backend()
    )

    signature = private_key.sign(
        data_bytes,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    encrypted_data = public_key.encrypt(
        data_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # convert to string(base64)
    encrypted_data_base64 = base64.b64encode(encrypted_data).decode('utf-8')
    signature_base64 = base64.b64encode(signature).decode('utf-8')

    body_content = {
        'data': encrypted_data_base64,
        'signature': signature_base64,
    }
    pprint.pprint({
        'received_encrypted_data_base64': encrypted_data_base64,
        'received_signature_base64': signature_base64,
        'received_encrypted_data': encrypted_data,
        'received_signature': signature
    })
    headers_content = json.loads(callback_headers)

    if callback_method == 'GET':
        requests.get(
            url=callback_url,
            json=body_content,
            headers=headers_content
        )
    elif callback_method == 'POST':
        requests.post(
            url=callback_url,
            json=body_content,
            headers=headers_content
        )
    elif callback_method == 'PUT':
        requests.put(
            url=callback_url,
            json=body_content,
            headers=headers_content
        )
    elif callback_method == 'PATCH':
        requests.patch(
            url=callback_url,
            json=body_content,
            headers=headers_content
        )
    elif callback_method == 'DELETE':
        requests.delete(
            url=callback_url,
            json=body_content,
            headers=headers_content
        )


# update one
class OrderAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAdminUser, )

    def patch(self, request, *args, **kwargs):
        logger.info(f'order patch, status={request.data["status"]}', exc_info=1)
        if request.data['status'] and request.data['status'] == 5:
            instance = self.get_object()

        date_format = '%Y-%m-%d %H:%M:%S'
        date_str = instance.date.strftime(date_format)

        custom_body_props = json.loads(instance.callbackBody)
        order_body = {
            'date': date_str,
            'orderId': instance.orderId,
            'card': instance.card,
            "payoutAmount": instance.payoutAmount,
            'screenshot': instance.screenshot,
            'compensation': instance.compensation
        }

        combined_body = {
            **custom_body_props,
            **order_body
        }
        data_bytes = json.dumps(combined_body, cls=DecimalEncoder).encode('utf-8')

        send_callback(
            callback_url=instance.callbackUrl,
            callback_method=instance.callbackMethod,
            callback_headers=instance.callbackHeaders,
            data_bytes=data_bytes,
        )

        return super().patch(request, *kwargs, *args)

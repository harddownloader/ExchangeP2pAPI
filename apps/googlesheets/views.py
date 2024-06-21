import os
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .tasks import run_partner_radar_task

class CreateGSTaskAPIView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request, *args, **kwargs):
        requests.get(
            os.getenv('APP_SCRIPT_ENDPOINT')
        )

        return Response('Done. Request send successfully.')

    def post(self, request, *args, **kwargs):
        run_partner_radar_task.delay()

        return Response('Done. Task sent successfully.')

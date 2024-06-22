import json
import os
import requests
import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from pymongo import MongoClient
from bson import json_util

from django.conf import settings
from .tasks import run_partner_radar_task


class GSCreateTaskAPIView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request, *args, **kwargs):
        try:
            collection = settings.APP_MONGO_CLIENT.google_sheets_config

            # is triggers active
            is_active_trigger_gs_record = collection.find_one({"name": "is_active_trigger_gs"})
            is_active_trigger_gs = is_active_trigger_gs_record['is_active_trigger_gs']
            logging.info(f"is_active_trigger_gs is {is_active_trigger_gs}")

            # get and use trigger info
            dashboard_radars_runner_record = collection.find_one({"name": "dashboard_radars_runner"})
            url = dashboard_radars_runner_record['endpoint']['url']
            method = dashboard_radars_runner_record['endpoint']['method']
            logging.info(f"dashboard radars URL: {url}")
            logging.info(f"dashboard radars METHOD: {method}")
            if (is_active_trigger_gs):
                r = requests.get(url)
                logging.info(f"request status: {r.status_code}")

                return Response('Done. Request send successfully.')

            return Response('Something went wrong.', status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response('error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            run_partner_radar_task.delay()

            return Response('Done. Task sent successfully.')
        except Exception as e:
            return Response('error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GSConfigAPIView(APIView):
    permission_classes = (IsAdminUser,)
    def get(self, request, *args, **kwargs):
        try:
            collection = settings.APP_MONGO_CLIENT.google_sheets_config
            is_active_trigger_gs_record = collection.find_one({"name": "is_active_trigger_gs"})
            is_active_trigger_gs = is_active_trigger_gs_record['is_active_trigger_gs']

            return Response({'is_active_trigger_gs': is_active_trigger_gs})
        except Exception as e:
            logging.error(e)
            return Response('error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, *args, **kwargs):
        try:
            logging.info(request.data)
            is_active_trigger_gs = request.data['is_active_trigger_gs']

            collection = settings.APP_MONGO_CLIENT.google_sheets_config

            if (isinstance(is_active_trigger_gs, bool)):
                filter = {'name': 'is_active_trigger_gs'}
                new_values = {"$set": {'is_active_trigger_gs': is_active_trigger_gs}}
                collection.update_one(filter, new_values)
                updatedConfigDoc = collection.find_one(filter)
                return Response(json.loads(json_util.dumps(updatedConfigDoc)))

            return Response('Something s wrong.', status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.error(e)
            return Response('error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

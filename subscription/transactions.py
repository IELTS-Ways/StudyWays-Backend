from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.views.permissions import IsInstitute, IsFreelance, IsStudent, IsMarketer
from accounts.models import InstituteProfile, StudentProfile, FreelanceProfile, MarketerPanel
from subscription.serializers import SubscriptionSerializer
from subscription.models import Subscription, DefaultPrice
import json
import requests
from django.conf import settings
from django.db import transaction
from config.responses import bad_request, SuccessResponse, UnsuccessfulResponse
from django.http import HttpResponse,JsonResponse
from datetime import datetime



class FreelanceTransactions(APIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsFreelance]

    def get(self, *args, **kwargs):
        try:
            freelance = FreelanceProfile.objects.get(user=self.request.user)
            sub = Subscription.objects.filter(freelance=freelance)
            serializer = self.serializer_class(sub, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("Subscription not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)




class MarketerTransactions(APIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsMarketer]

    def get(self, *args, **kwargs):
        try:
            marketer = MarketerPanel.objects.get(user=self.request.user)
            # should add lines...
            sub = Subscription.objects.filter(freelance=marketer)
            serializer = self.serializer_class(sub, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("Subscription not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)
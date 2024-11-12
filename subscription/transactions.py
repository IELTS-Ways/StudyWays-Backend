from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from accounts.views.permissions import IsInstitute, IsFreelance, IsStudent, IsMarketer
from accounts.models import InstituteProfile, StudentProfile, FreelanceProfile, MarketerPanel
from subscription.serializers import SubscriptionSerializer, FreelanceTransactionsSerializer, InstituteTransactionsSerializer
from subscription.models import Subscription, DefaultPrice
import json
import requests
from django.conf import settings
from django.db import transaction
from config.responses import bad_request, SuccessResponse, UnsuccessfulResponse
from django.http import HttpResponse,JsonResponse
from datetime import datetime
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class FreelanceTransactions(GenericAPIView):
    permission_classes = [IsFreelance]
    queryset = Subscription.objects.all()
    pagination_class = CustomPagination
    serializer_class = FreelanceTransactionsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['type', 'status', 'user', 'day_period', 'price', 'created_at', 'paid', 'description', 'ref_id', 'apportionment_percentage', 'freelance_price']
    search_fields = ['type', 'status','day_period', 'price', 'created_at', 'paid', 'description', 'ref_id', 'apportionment_percentage', 'freelance_price']
    ordering_fields = ['type', 'status', 'user', 'day_period', 'price', 'created_at', 'paid', 'description', 'ref_id', 'apportionment_percentage', 'freelance_price']

    def get(self, *args, **kwargs):
        freelance = FreelanceProfile.objects.get(user=self.request.user)
        trans = self.filter_queryset(Subscription.objects.filter(freelance=freelance))
        page = self.paginate_queryset(trans)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.filter_queryset(Subscription.objects.filter(freelance=freelance))
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    
class InstituteTransactions(GenericAPIView):
    permission_classes = [IsInstitute]
    queryset = Subscription.objects.all()
    pagination_class = CustomPagination
    serializer_class = InstituteTransactionsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['type', 'status', 'user', 'day_period', 'price', 'created_at', 'paid', 'description', 'ref_id', 'apportionment_percentage', 'institute_price']
    search_fields = ['type', 'status','day_period', 'price', 'created_at', 'paid', 'description', 'ref_id', 'apportionment_percentage', 'institute_price']
    ordering_fields = ['type', 'status', 'user', 'day_period', 'price', 'created_at', 'paid', 'description', 'ref_id', 'apportionment_percentage', 'institute_price']

    def get(self, *args, **kwargs):
        institute = InstituteProfile.objects.get(user=self.request.user)
        trans = self.filter_queryset(Subscription.objects.filter(institute=institute))
        page = self.paginate_queryset(trans)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.filter_queryset(Subscription.objects.filter(institute=institute))
        return Response(serializer.data, status=status.HTTP_200_OK)



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
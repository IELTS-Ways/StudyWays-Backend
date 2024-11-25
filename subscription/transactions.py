from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from accounts.views.permissions import IsInstitute, IsFreelance, IsStudent, IsMarketer
from accounts.models import InstituteProfile, StudentProfile, FreelanceProfile, MarketerPanel, User
from subscription.serializers import SubscriptionSerializer, FreelanceTransactionsSerializer, InstituteTransactionsSerializer, InviterTransactionsSerializer, WithdrawRequestSerializer
from subscription.models import Subscription, DefaultPrice, Withdraw
from subscription.views import WithdrawRequest
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
    search_fields = ['type', 'status', 'day_period', 'price', 'created_at', 'paid', 'description', 'ref_id', 'apportionment_percentage', 'freelance_price']
    ordering_fields = ['type', 'status', 'user', 'day_period', 'price', 'created_at', 'paid', 'description', 'ref_id', 'apportionment_percentage', 'freelance_price']

    def get(self, request, *args, **kwargs):
        freelance = FreelanceProfile.objects.get(user=request.user)
        
        trans = self.filter_queryset(Subscription.objects.filter(freelance=freelance))
        subscriptions_page = self.paginate_queryset(trans)
        subscriptions_data = self.serializer_class(subscriptions_page, many=True).data if subscriptions_page else []

        withdraw_requests = Withdraw.objects.filter(user=request.user)
        withdraw_status = request.query_params.get('withdraw_status')
        if withdraw_status:
            withdraw_requests = withdraw_requests.filter(status=withdraw_status)
        
        withdraw_order = request.query_params.get('withdraw_ordering', None)
        if withdraw_order:
            withdraw_requests = withdraw_requests.order_by(withdraw_order)
            
        withdraw_requests_page = self.paginate_queryset(withdraw_requests)
        withdraw_requests_data = WithdrawRequestSerializer(withdraw_requests_page, many=True).data if withdraw_requests_page else []

        results = {
            "subscriptions": subscriptions_data,
            "withdraw_requests": withdraw_requests_data,
        }

        if subscriptions_page or withdraw_requests_page:
            return self.get_paginated_response(results)

        return Response(results, status=status.HTTP_200_OK)



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



class MarketerTransactions(GenericAPIView):
    permission_classes = [IsMarketer]
    queryset = Subscription.objects.all()
    pagination_class = CustomPagination
    serializer_class = InviterTransactionsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['type', 'status', 'user', 'day_period', 'price', 'created_at', 'paid', 'description', 'ref_id','inviter_sales_percentage', 'inviter_price']
    search_fields = ['type', 'status','day_period', 'price', 'created_at', 'paid', 'description', 'ref_id', 'inviter_sales_percentage', 'inviter_price']
    ordering_fields = ['type', 'status', 'user', 'day_period', 'price', 'created_at', 'paid', 'description', 'ref_id','inviter_sales_percentage', 'inviter_price']
    
    def get(self, request, *args, **kwargs):
        sender = User.objects.get(id=self.request.user.id)
        invite_code = sender.invite_code
        invited_user = self.filter_queryset(Subscription.objects.filter(user__user__invite_code=invite_code))
        subscriptions_page = self.paginate_queryset(invited_user)
        subscriptions_data = self.serializer_class(subscriptions_page, many=True).data if subscriptions_page else []

        withdraw_requests = Withdraw.objects.filter(user=request.user)
        withdraw_status = request.query_params.get('withdraw_status')
        if withdraw_status:
            withdraw_requests = withdraw_requests.filter(status=withdraw_status)
        
        withdraw_order = request.query_params.get('withdraw_ordering', None)
        if withdraw_order:
            withdraw_requests = withdraw_requests.order_by(withdraw_order)
            
        withdraw_requests_page = self.paginate_queryset(withdraw_requests)
        withdraw_requests_data = WithdrawRequestSerializer(withdraw_requests_page, many=True).data if withdraw_requests_page else []

        results = {
            "subscriptions": subscriptions_data,
            "withdraw_requests": withdraw_requests_data,
        }

        if subscriptions_page or withdraw_requests_page:
            return self.get_paginated_response(results)

        return Response(results, status=status.HTTP_200_OK)
    
    # def get(self, *args, **kwargs):
    #     sender = User.objects.get(id=self.request.user.id)
    #     invite_code = sender.invite_code
    #     invited_user = self.filter_queryset(Subscription.objects.filter(user__user__invite_code=invite_code))
    #     page = self.paginate_queryset(invited_user)
    #     if page is not None:
    #         serializer = self.serializer_class(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #     serializer = self.filter_queryset(Subscription.objects.filter(user__user__invite_code=invite_code))
    #     return Response(serializer.data, status=status.HTTP_200_OK)


class StudentTransactions(GenericAPIView):
    permission_classes = [IsStudent]
    queryset = Subscription.objects.all()
    pagination_class = CustomPagination
    serializer_class = InviterTransactionsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['type', 'status', 'user', 'day_period', 'price', 'created_at', 'paid', 'description', 'ref_id','inviter_sales_percentage', 'inviter_price']
    search_fields = ['type', 'status','day_period', 'price', 'created_at', 'paid', 'description', 'ref_id', 'inviter_sales_percentage', 'inviter_price']
    ordering_fields = ['type', 'status', 'user', 'day_period', 'price', 'created_at', 'paid', 'description', 'ref_id','inviter_sales_percentage', 'inviter_price']

    def get(self, *args, **kwargs):
        sender = User.objects.get(id=self.request.user.id)
        invite_code = sender.invite_code
        invited_user = self.filter_queryset(Subscription.objects.filter(user__user__invite_code=invite_code))
        page = self.paginate_queryset(invited_user)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.filter_queryset(Subscription.objects.filter(user__user__invite_code=invite_code))
        return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from accounts.views.permissions import IsInstitute, IsFreelance, IsStudent, IsMarketer
from accounts.models import InstituteProfile, StudentProfile, FreelanceProfile, MarketerPanel, User
from service.serializers import ServiceHistorySerializer
from service.models import Service, ReportSharing
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


class StudentHistory(GenericAPIView):
    permission_classes = [IsStudent]
    queryset = Service.objects.all()
    pagination_class = CustomPagination
    serializer_class = ServiceHistorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['type', 'user', 'file', 'text', 'done', 'start_time', 'end_time', 'duration', 'word_count','slash_count','average','missing_words','created_at']
    search_fields = ['type', 'text', 'done', 'start_time', 'end_time', 'duration', 'word_count','slash_count','average','missing_words','created_at']
    ordering_fields = ['type', 'user', 'file', 'text', 'done', 'start_time', 'end_time', 'duration', 'word_count','slash_count','average','missing_words','created_at']
    ordering = ['-created_at']

    def get(self, *args, **kwargs):
        user = StudentProfile.objects.get(user=self.request.user)
        history = self.filter_queryset(Service.objects.filter(user=user))
        page = self.paginate_queryset(history)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.filter_queryset(Service.objects.filter(user=user))
        return Response(serializer.data, status=status.HTTP_200_OK)

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
    filterset_fields = ['type', 'user', 'file', 'text', 'done', 'start_time', 'end_time', 'duration', 'word_count', 'slash_count', 'average', 'missing_words', 'created_at']
    search_fields = ['type', 'text', 'done', 'start_time', 'end_time', 'duration', 'word_count', 'slash_count', 'average', 'missing_words', 'created_at']
    ordering_fields = ['type', 'user', 'file', 'text', 'done', 'start_time', 'end_time', 'duration', 'word_count', 'slash_count', 'average', 'missing_words', 'created_at']
    ordering = ['-created_at']

    def create_share_link(self, service, user):
        report_sharing = ReportSharing.objects.filter(
            user=user,
            report=service,
            access_type='allow_any',
        ).first()
        if not report_sharing:
            report_sharing = ReportSharing.objects.create(
                user=user,
                report=service,
                access_type='allow_any',
            )
            report_sharing.generate_dynamic_link()
            report_sharing.save()
        return report_sharing.link

    def get(self, *args, **kwargs):
        user = StudentProfile.objects.get(user=self.request.user)
        history = self.filter_queryset(Service.objects.filter(user=user))
        page = self.paginate_queryset(history)

        if page is not None:
            data = []
            for service in page:
                share_link = self.create_share_link(service, user)
                serializer = self.serializer_class(service)
                serialized_data = serializer.data
                serialized_data['share_link'] = share_link
                data.append(serialized_data)
            return self.get_paginated_response(data)

        data = []
        for service in history:
            share_link = self.create_share_link(service, user)
            serializer = self.serializer_class(service)
            serialized_data = serializer.data
            serialized_data['share_link'] = share_link
            data.append(serialized_data)

        return Response(data, status=status.HTTP_200_OK)
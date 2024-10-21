from django.shortcuts import render
from .models import Contact, Application
from .serializers import ContactSerializer, ApplicationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ContactUsView(APIView):
    serializer_class = ContactSerializer
    
    def post(self, *args, **kwargs):
        data = self.request.data
        serializer = self.serializer_class(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
    
class ApplicationFormView(APIView):
    serializer_class = ApplicationSerializer
    
    def post(self, *args, **kwargs):
        data = self.request.data
        serializer = self.serializer_class(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

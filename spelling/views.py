from django.shortcuts import render
from .models import SpellingDrills
from .serializers import SpellingSerializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from accounts.views.permissions import IsInstitute, IsFreelance, IsStudent
from rest_framework import status
from accounts.models import StudentProfile

class Spelling(APIView):
    serializer_class = SpellingSerializers
    permission_classes = [IsStudent]

    def post(self, *args, **kwargs):
        data = self.request.data
        student = StudentProfile.objects.get(user=self.request.user)
        data["user"] = student.id
        serializer = self.serializer_class(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    def get(self, *args, **kwargs):
        try:
            student = StudentProfile.objects.get(user=self.request.user)
            data = SpellingDrills.objects.filter(user=student)
            serializer = self.serializer_class(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("Something went wrong, try again",status=status.HTTP_400_BAD_REQUEST)


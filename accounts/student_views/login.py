from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from config import responses
from accounts.functions import get_user_data, login
from config.settings import ACCESS_TTL
from accounts.serializers import UserSerializer,StudentProfileSerializer, InstituteSerializer
from django.contrib.auth import authenticate
from accounts.views.permissions import IsStudent
from rest_framework.permissions import AllowAny
from accounts.models.student_profile import StudentProfile, InstituteProfile


class StudentLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, *args, **kwargs):
        phone_number = self.request.data.get("phone_number")
        password = self.request.data.get("password")
        user = authenticate(phone_number=phone_number, password=password)

        if user is not None:
            access, refresh = login(user)
        else:
            return Response("phone_number or password is incorrect", status=status.HTTP_406_NOT_ACCEPTABLE)

        data = {
            "refresh_token": refresh,
            "access_token": access,
            "user_data": UserSerializer(user).data,
        }
        response = Response(
            {
                "success": True,
                "data": data,
            },
            status=status.HTTP_200_OK,
        )
        response.set_cookie(
            "HTTP_ACCESS",
            f"Bearer {access}",
            max_age=ACCESS_TTL * 24 * 3600,
            secure=True,
            httponly=True,
            samesite="None",
        )
        return response





class StudentOverview(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsStudent]

    def get(self, *args, **kwargs):
        user=self.request.user
        student = StudentProfile.objects.get(user=user)
        data = {
            "user": self.serializer_class(user).data,
            "student": StudentProfileSerializer(student).data,
            "institute": InstituteSerializer(student.institute).data,
            "payments": None,
        }
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, *args, **kwargs):
        user = self.request.user
        student = StudentProfile.objects.get(user=user)
        serializer = StudentProfileSerializer(student, data=self.request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)




class StudentInstituteData(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsStudent]

    def get(self, *args, **kwargs):
        user=self.request.user
        student = StudentProfile.objects.get(user=user)
        data = InstituteSerializer(student.institute).data
        return Response(data, status=status.HTTP_200_OK)
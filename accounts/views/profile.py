from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.functions import get_user_data, login
from accounts.models import OneTimePassword
from accounts.selectors import get_user
from config.settings import ACCESS_TTL
from accounts.serializers import UserSerializer, UserAllFieldsSerializer, UserUpdateSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
import re
from django.utils.translation import gettext as _
from rest_framework.throttling import AnonRateThrottle
from accounts.functions import send_sms_otp
from accounts.models import OneTimePassword,User,InstituteProfile,MarketerPanel,FreelanceProfile,StudentProfile



class Profile(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        serializer = self.serializer_class(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, *args, **kwargs):
        data = self.request.data
        profile = User.objects.get(id=self.request.user.id)
        serializer = UserUpdateSerializer(profile, data=data)
        if serializer.is_valid():
            serializer.save()
            user = self.request.user

            if user.user_type == "freelance":
                FreelanceProfile.objects.get_or_create(user=user)
            elif user.user_type == "institute":
                InstituteProfile.objects.get_or_create(user=user)
            elif user.user_type == "marketer":
                MarketerPanel.objects.get_or_create(user=user)
            elif user.user_type == "student":
                try:
                    student, created = StudentProfile.objects.get_or_create(user=user)
                    inviter = User.objects.get(id=int(data["invite_code"]))
                    if inviter.user_type == "freelance":
                        freelance_parent = FreelanceProfile.objects.get(user=inviter)
                        student.freelance = freelance_parent
                        student.save()
                    elif inviter.user_type == "institute":
                        institute_parent = InstituteProfile.objects.get(user=inviter)
                        student.institute = institute_parent
                        student.save()
                    else:
                        institute_parent = InstituteProfile.objects.get(id=8)
                        student.institute = institute_parent
                        student.save()
                except:
                    return Response("Parent not found or somthing wrong...", status=status.HTTP_406_NOT_ACCEPTABLE)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


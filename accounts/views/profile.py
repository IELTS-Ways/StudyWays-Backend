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
import logging


logger = logging.getLogger(__name__)


class Profile(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        serializer = self.serializer_class(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, *args, **kwargs):
        data = self.request.data
        user = self.request.user
        serializer = UserUpdateSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            if user.user_type == "freelance":
                FreelanceProfile.objects.get_or_create(user=user)
            elif user.user_type == "institute":
                InstituteProfile.objects.get_or_create(user=user)
            elif user.user_type == "marketer":
                MarketerPanel.objects.get_or_create(user=user)
            elif user.user_type == "student":
                student, created = StudentProfile.objects.get_or_create(user=user)
                invite_code = data["invite_code"]
                if invite_code:
                    inviter = User.objects.get(id=invite_code)
                    if inviter.user_type == "freelance":
                        freelance_parent = FreelanceProfile.objects.get(user=inviter)
                        student.freelance = freelance_parent
                    elif inviter.user_type == "institute":
                        institute_parent = InstituteProfile.objects.get(user=inviter)
                        student.institute = institute_parent
                    else:
                        institute_parent = InstituteProfile.objects.get(id=79)
                        student.institute = institute_parent
                student.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

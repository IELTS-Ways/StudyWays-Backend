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

    def patch(self, request, *args, **kwargs):
        data = self.request.data
        profile = User.objects.get(id=self.request.user.id)
        # user_id = request.data.get("user_id")
        invite_code = request.data.get("invite_code")

        user = User.objects.filter(id=invite_code).first()
        
        if not user:
            return Response({"detail": "Invite code not found."}, status=status.HTTP_404_NOT_FOUND)
        
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
                if data["parent"] == "freelance":
                    StudentProfile.objects.get_or_create( user=user, freelance=FreelanceProfile.objects.get(id=data["parent_id"]) )
                elif data["parent"] == "institute":
                    StudentProfile.objects.get_or_create( user=user, institute=InstituteProfile.objects.get(id=data["parent_id"]) )
                elif data["parent"] == "not":
                    StudentProfile.objects.get_or_create( user=user, institute=InstituteProfile.objects.get(id=10) )
                else:
                    StudentProfile.objects.get_or_create( user=user, institute=InstituteProfile.objects.get(id=10) )

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

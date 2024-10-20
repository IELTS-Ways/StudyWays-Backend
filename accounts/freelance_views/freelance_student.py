from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from subscription.models import Subscription
from subscription.serializers import SubscriptionSerializer
from accounts.serializers import UserSerializer, FreelanceProfileSerializer, StudentProfileSerializer
from accounts.models import User,FreelanceProfile, StudentProfile
from accounts.views.permissions.is_freelance import IsFreelance


class FreelanceStudent(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsFreelance]

    def get(self, *args, **kwargs):
        data = []
        freelance = FreelanceProfile.objects.get(user=self.request.user)
        student = StudentProfile.objects.filter(freelance=freelance)
        for obj in student:
            student_serializer = StudentProfileSerializer(obj)
            student_sub = Subscription.objects.filter(user=obj,paid=True)
            sub_serializer = SubscriptionSerializer(student_sub,many=True)
            student_data = {"student":student_serializer.data, "subscription":sub_serializer.data}
            data.append(student_data)
        #serializer = StudentProfileSerializer(student,many=True)
        return Response(data, status=status.HTTP_200_OK)

    def post(self, *args, **kwargs):
        data = self.request.data
        data["password"] = "12345678"
        data["user_type"] = "student"
        serializer = self.serializer_class(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            student_user = User.objects.get(id=serializer.data["id"])
            student_user.set_password(data["password"])
            student_user.save()
            student_profile = StudentProfile.objects.get(user=student_user)
            student_profile.freelance = FreelanceProfile.objects.get(user=self.request.user)
            student_profile.gender = data["gender"]
            student_profile.english_level = data["english_level"]
            student_profile.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

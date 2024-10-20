from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.serializers import UserSerializer, InstituteSerializer, StudentProfileSerializer
from accounts.models import User,InstituteProfile,StudentProfile
from accounts.views.permissions.is_institute import IsInstitute
from accounts.models.institute_profile import InstituteProfile
from rest_framework.permissions import AllowAny, IsAuthenticated
from subscription.models import Subscription
from subscription.serializers import SubscriptionSerializer

class InstituteStudent(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsInstitute]

    def get(self, *args, **kwargs):
        data = []
        institute = InstituteProfile.objects.get(user=self.request.user)
        student = StudentProfile.objects.filter(institute=institute)
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
            student_profile.institute = InstituteProfile.objects.get(user=self.request.user)
            student_profile.gender = data["gender"]
            student_profile.english_level = data["english_level"]
            student_profile.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)





class InstituteStudentMultiple(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsInstitute]

    def post(self, *args, **kwargs):
        print('=====')
        print(self.request.FILES['excel_file'])


        excel_file = self.request.FILES['excel_file']
        # Load the workbook and access the active worksheet
        wb = openpyxl.load_workbook(excel_file)
        ws = wb.active

        # Iterate through rows and extract data
        for row in ws.iter_rows(min_row=2, values_only=True):
            model, serial, hd_size, ram, processor = row
            # Process the data as needed (e.g., create objects or update existing


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
            student_profile.institute = InstituteProfile.objects.get(user=self.request.user)
            student_profile.gender = data["gender"]
            student_profile.english_level = data["english_level"]
            student_profile.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

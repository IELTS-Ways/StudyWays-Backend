from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.serializers import UserSerializer, InstituteSerializer, StudentProfileSerializer, UserUpdateSerializer
from accounts.serializers.student import MultipleStudentProfileSerializer
from accounts.models import User,InstituteProfile,StudentProfile
from accounts.views.permissions.is_institute import IsInstitute
from accounts.models.institute_profile import InstituteProfile
from rest_framework.permissions import AllowAny, IsAuthenticated
from subscription.models import Subscription
from subscription.serializers import SubscriptionSerializer
from datetime import datetime
import pandas as pd


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
            student_profile.education = data["education"]
            student_profile.majors_name = data["majors_name"]
            student_profile.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)





class InstituteStudentMultiple(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsInstitute]  
    
    def post(self, request, *args, **kwargs):

        excel_file = self.request.FILES.get('file')
        users_data = []
        students = []    
        df = pd.read_excel(excel_file, dtype={'Phone Number': str})
            
        for _, row in df.iterrows():
            date_value = row['Birth Date']  # Birth date
            if isinstance(date_value, datetime):
                date_value = date_value.date()

            user_data = {
                'phone_number': row['Phone Number'],
                'first_name': row['First Name'],
                'last_name': row['Last Name'],
                'birth_date': date_value,
            }
            users_data.append(user_data)                
        user_serializer = UserSerializer(data=users_data, many=True)
        if user_serializer.is_valid():
            users = user_serializer.save()       
                     
            for i, row in enumerate(df.iterrows()):
                student_data = {
                    'user': users[i].id, 
                    'gender': row[1]['Gender'],
                    'english_level': row[1]['English Level'],
                    'institute': self.request.user.id
                }        
                students.append(student_data)
            student_serializer = MultipleStudentProfileSerializer(data=students, many=True)
            if student_serializer.is_valid():
                student_serializer.save()
                for user in users:
                    user.user_type = 'student'
                    user.set_password('12345678')
                    user.save() 
                    
                return Response({"message": "Success"}, status=200)
            else:
                print("Student serializer errors:", student_serializer.errors)
                return Response({"message": "Error", "errors": student_serializer.errors}, status=400)
        else:
            return Response({"message": "Error", "errors": user_serializer.errors}, status=400)





class InstituteStudentItem(APIView):
    serializer_class = StudentProfileSerializer
    permission_classes = [IsInstitute]
    def get(self, *args, **kwargs):
        try:
            institute = InstituteProfile.objects.get(user=self.request.user)
            student = StudentProfile.objects.get(id=self.kwargs["id"],institute=institute)
            serializer = self.serializer_class(student)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("Student not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)

    def patch(self, *args, **kwargs):
        try:
            institute = InstituteProfile.objects.get(user=self.request.user)
            student = StudentProfile.objects.get(id=self.kwargs["id"],institute=institute)

            user_serializer = UserUpdateSerializer(student.user, data=self.request.data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()

            serializer = self.serializer_class(student, data=self.request.data, partial=True)
            if serializer.is_valid():
                serializer.save()

                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response("Student not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, *args, **kwargs):
        try:
            institute = InstituteProfile.objects.get(user=self.request.user)
            student = StudentProfile.objects.get(id=self.kwargs["id"],institute=institute)
            base_user = student.user
            student.delete()
            base_user.delete()
            return Response("Student deleted.", status=status.HTTP_200_OK)
        except:
            return Response("Student not found or something went wrong, try again.", status=status.HTTP_400_BAD_REQUEST)


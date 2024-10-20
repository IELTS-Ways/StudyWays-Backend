from rest_framework import serializers
from accounts.models.student_profile import StudentProfile
from accounts.serializers.user import UserSerializer

class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = StudentProfile
        fields = "__all__"

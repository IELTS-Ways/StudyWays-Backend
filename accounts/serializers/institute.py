from rest_framework import serializers
from accounts.models.institute_profile import InstituteProfile


class InstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstituteProfile
        fields = "__all__"


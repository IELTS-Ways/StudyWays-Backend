from rest_framework import serializers
from accounts.models.freelance_profile import FreelanceProfile

class FreelanceProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreelanceProfile
        fields = "__all__"
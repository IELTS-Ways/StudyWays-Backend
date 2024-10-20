from rest_framework import serializers
from accounts.models.marketer_panel import MarketerPanel
from accounts.serializers.user import UserAllFieldsSerializer
class MarketerPanelSerializer(serializers.ModelSerializer):
    user=UserAllFieldsSerializer(read_only=True)
    class Meta:
        model = MarketerPanel
        fields = "__all__"
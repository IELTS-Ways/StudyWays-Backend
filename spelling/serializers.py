from rest_framework import serializers
from .models import SpellingDrills


class SpellingSerializers(serializers.ModelSerializer):
    class Meta:
        model = SpellingDrills
        fields = '__all__'




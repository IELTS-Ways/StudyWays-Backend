from rest_framework import serializers
from subscription.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        #fields = "__all__"
        fields = ("id", "type", "day_period", "price", "created_at", "user", "expierd")

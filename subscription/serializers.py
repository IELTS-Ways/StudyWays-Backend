from rest_framework import serializers
from subscription.models import Subscription, Withdraw, DiscountCode


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        #fields = "__all__"
        fields = ("id", "type", "day_period", "price", "created_at", "user", "expired")
        
class FreelanceTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('type', 'status', 'user', 'day_period', 'price', 'created_at', 'paid', 'description', 'ref_id', 'apportionment_percentage', 'freelance_price')
        
        
class InstituteTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('type', 'status', 'user', 'day_period', 'price', 'created_at', 'paid', 'description', 'ref_id', 'apportionment_percentage', 'institute_price','discount_amount')
        
        
class InviterTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('type', 'status', 'user', 'day_period', 'price', 'created_at', 'paid', 'description', 'ref_id', 'inviter_sales_percentage', 'inviter_price')


class WithdrawRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdraw
        fields = '__all__'
        
class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = '__all__'
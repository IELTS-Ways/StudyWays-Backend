from django.contrib import admin
from subscription.models import Subscription,DefaultPrice, Withdraw, FreeTrial, DiscountCode
from import_export.admin import ImportExportModelAdmin


class SubscriptionAdmin(ImportExportModelAdmin):
    list_display = ('type', 'user', 'created_at', "institute", 'expired', 'status', 'remaining_days','price','institute_price')
    list_filter = ("type", "created_at", "status","institute","freelance")
admin.site.register(Subscription, SubscriptionAdmin)


class DefaultPriceAdmin(ImportExportModelAdmin):
    list_display = ('audio_video_scripter', 'memory_mirror', 'planner', 'fast_reading', 'id')
admin.site.register(DefaultPrice, DefaultPriceAdmin)


class WithdrawAdmin(ImportExportModelAdmin):
    list_display = ('user', 'status', 'created_at', 'price')
    list_filter = ("status", "created_at")
admin.site.register(Withdraw, WithdrawAdmin)


class FreeTrialAdmin(ImportExportModelAdmin):
    list_display = ('user', 'is_active', 'remaining_days')
    list_filter = ("is_active",)
admin.site.register(FreeTrial, FreeTrialAdmin)

class DiscountCodeAdmin(ImportExportModelAdmin):
    list_display = ('code', 'discount_percentage', 'status', 'limit_days', 'days_remaining', 'usage_limit', 'usage_count')
    list_filter = ("status",)
    search_fields = ['code', 'discount_percentage', 'limit_days', 'usage_limit']
admin.site.register(DiscountCode, DiscountCodeAdmin)

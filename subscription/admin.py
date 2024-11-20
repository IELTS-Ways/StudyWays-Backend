from django.contrib import admin
from subscription.models import Subscription,DefaultPrice, Withdraw
from import_export.admin import ImportExportModelAdmin

class SubscriptionAdmin(ImportExportModelAdmin):
    list_display = ('type', 'user', 'created_at', 'expired', 'status', 'remaining_days')
    list_filter = ("type", "created_at", "status")
admin.site.register(Subscription, SubscriptionAdmin)


class DefaultPriceAdmin(ImportExportModelAdmin):
    list_display = ('audio_video_scripter', 'memory_mirror', 'planner', 'fast_reading', 'id')
admin.site.register(DefaultPrice, DefaultPriceAdmin)

class WithdrawAdmin(ImportExportModelAdmin):
    list_display = ('user', 'status', 'created_at', 'price')
    list_filter = ("status", "created_at")
admin.site.register(Withdraw, WithdrawAdmin)


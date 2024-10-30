from django.contrib import admin
from subscription.models import Subscription
from import_export.admin import ImportExportModelAdmin

class SubscriptionAdmin(ImportExportModelAdmin):
    list_display = ('type', 'user', 'created_at', 'expired', 'status', 'remaining_days')
admin.site.register(Subscription, SubscriptionAdmin)

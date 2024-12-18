from django.contrib import admin
from service.models import Service, MultipleSpellings, HyphenatedAdjectives, FeedbackSystem, ReportSharing
from import_export.admin import ImportExportModelAdmin


class ServiceAdmin(ImportExportModelAdmin):
    list_display = ('type', 'user', 'created_at', 'done')
    list_filter = ("type", "user", "done")
    search_fields = ['type']
admin.site.register(Service, ServiceAdmin)


class MultipleSpellingsAdmin(ImportExportModelAdmin):
    list_display = ('id','UK', 'US')
    search_fields = ['UK','US']
admin.site.register(MultipleSpellings, MultipleSpellingsAdmin)


class HyphenatedAdjectivesAdmin(ImportExportModelAdmin):
    list_display = ('id','US',)
    search_fields = ['US',]
admin.site.register(HyphenatedAdjectives, HyphenatedAdjectivesAdmin)


class FeedbackSystemAdmin(ImportExportModelAdmin):
    list_display = ('user','star','created_at')
    list_filter = ("star", "user", "created_at")
admin.site.register(FeedbackSystem, FeedbackSystemAdmin)


class ReportShareAdmin(ImportExportModelAdmin):
    list_display = ('link','user','created_at','access_type', 'report')
    list_filter = ("created_at",'access_type')
    search_fields = ['access_type', 'report', 'link']
admin.site.register(ReportSharing, ReportShareAdmin)

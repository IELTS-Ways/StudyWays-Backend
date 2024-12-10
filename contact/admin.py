from django.contrib import admin
from .models import Contact, Application
from import_export.admin import ImportExportModelAdmin


class ContactAdmin(ImportExportModelAdmin):
    list_display = ('title', 'name', 'email')
    list_filter = ("created_at",)
    search_fields = ['title', 'name', 'email', 'description']
admin.site.register(Contact, ContactAdmin)


class ApplicationAdmin(ImportExportModelAdmin):
    list_display = ('full_name', 'phone_number', 'email')
    list_filter = ("location",)
    search_fields = ['full_name', 'phone_number', 'email', 'question', 'location']
admin.site.register(Application, ApplicationAdmin)
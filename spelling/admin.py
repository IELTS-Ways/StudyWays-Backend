from django.contrib import admin
from .models import SpellingDrills
from import_export.admin import ImportExportModelAdmin


class SpellingAdmin(ImportExportModelAdmin):
    list_display = ('words', 'user', 'created_at')
    list_filter = ("user", "created_at")
    search_fields = ['words']
admin.site.register(SpellingDrills, SpellingAdmin)
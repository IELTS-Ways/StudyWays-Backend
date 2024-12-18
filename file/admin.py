from django.contrib import admin
from file.models import File
from import_export.admin import ImportExportModelAdmin


class FileAdmin(ImportExportModelAdmin):
    list_display = ('id', 'book_type', 'book', 'unit', 'page', 'cd', 'track')
    list_filter = ("book_type", "CEFR", "skill_type", "material_type", "language")
    search_fields = ['book_type', 'book', 'unit']
admin.site.register(File, FileAdmin)


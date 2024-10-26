from django.contrib import admin
from accounts.models import User, StudentProfile, FreelanceProfile, InstituteProfile, MarketerPanel, MarketerWallet, FreelanceWallet
from import_export.admin import ImportExportModelAdmin


class UserAdmin(ImportExportModelAdmin):
    list_display = ('phone_number', 'created_at')
admin.site.register(User, UserAdmin)

class StudentProfileAdmin(ImportExportModelAdmin):
    list_display = ("user", "institute", "is_IELTS_student")
admin.site.register(StudentProfile, StudentProfileAdmin)

class InstituteProfileAdmin(ImportExportModelAdmin):
    list_display = ("user", "school_name", "username")
admin.site.register(InstituteProfile, InstituteProfileAdmin)

class FreelanceProfileAdmin(ImportExportModelAdmin):
    list_display = ("user", "school_name", "username")
admin.site.register(FreelanceProfile, FreelanceProfileAdmin)

class MarketerPanelAdmin(ImportExportModelAdmin):
    list_display = ("user", "province")
admin.site.register(MarketerPanel, MarketerPanelAdmin)

class MarketerWalletAdmin(ImportExportModelAdmin):
    list_display = ("user", "balance", "updated_at")
admin.site.register(MarketerWallet, MarketerWalletAdmin)

class FreelanceWalletAdmin(ImportExportModelAdmin):
    list_display = ("user", "balance", "updated_at")
admin.site.register(FreelanceWallet, FreelanceWalletAdmin)
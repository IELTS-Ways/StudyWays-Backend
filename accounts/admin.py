from django.contrib import admin
from accounts.models import User, StudentProfile, FreelanceProfile, InstituteProfile, MarketerPanel, MarketerWallet, FreelanceWallet
from accounts.models.student_profile import StudentWallet
from accounts.models.institute_profile import InstituteWallet
from import_export.admin import ImportExportModelAdmin


class UserAdmin(ImportExportModelAdmin):
    list_display = ('phone_number','user_type','email','id','is_profile_fill', 'created_at')
    list_filter = ("user_type", "confirmed", "created_at")
    search_fields = ['phone_number', 'first_name', 'last_name', 'email', 'username']
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

class StudentWalletAdmin(ImportExportModelAdmin):
    list_display = ("user", "balance", "updated_at")
admin.site.register(StudentWallet, StudentWalletAdmin)

class InstituteWalletAdmin(ImportExportModelAdmin):
    list_display = ("user", "balance", "updated_at")
admin.site.register(InstituteWallet, InstituteWalletAdmin)
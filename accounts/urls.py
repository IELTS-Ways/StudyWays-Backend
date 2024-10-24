from django.urls import path
from accounts.views import Logout,Profile,Refresh,RefreshAccess,OverView,SendOTP,VerifyOTP,UserValidationView
from accounts.student_views import StudentLogin,StudentOverview,StudentInstituteData
from accounts.institute_views import InstituteOverview,Institute,InstituteStudent,ZarinpalMerchantID,InstituteFull,\
    InstituteStudentMultiple,InstituteStudentItem,InstitutePricing
from accounts.freelance_views import FreelanceOverview,Freelance,FreelanceStudent,FreelanceFull,FreelanceStudentMultiple,\
    FreelanceStudentItem
from accounts.management_panel_view import InstituteLists,StudentLists,FreelanceLists
from accounts.visitors_views import InstituteLists as VisitList
from accounts.management_panel_view import InstituteLists,StudentLists,FreelanceLists
from accounts.marketer_views import MarketerOverview,MarketerFull,Marketers


urlpatterns = [
    path("otp", SendOTP.as_view(), name="send_otp"),
    path("otp/verify", VerifyOTP.as_view(), name="verify_otp"),
    path("refresh", Refresh.as_view(), name="refresh"),
    path("refresh-access", RefreshAccess.as_view(), name="refresh-access"),
    path("logout", Logout.as_view(), name="logout"),
    path("profile", Profile.as_view(), name="profile"),
    path("overview", OverView.as_view(), name="overview"),
    path("is-valid", UserValidationView.as_view(), name="is-valid"),
    #
    path("student-login", StudentLogin.as_view(), name="student-login"),
    path("student-overview", StudentOverview.as_view(), name="student-overview"),
    path("student-institute-data", StudentInstituteData.as_view(), name="student-institute-data"),
    #
    path("institute-overview", InstituteOverview.as_view(), name="institute-overview"),
    path("institute", Institute.as_view(), name="institute"),
    path("institute-full", InstituteFull.as_view(), name="institute-full"),
    path("institute-student", InstituteStudent.as_view(), name="institute-student"),
    path("institute-student-item/<int:id>", InstituteStudentItem.as_view(), name="institute-student-item"),
    path("institute-student-multiple", InstituteStudentMultiple.as_view(), name="institute-student-multiple"),
    path("zp-id", ZarinpalMerchantID.as_view(), name="zp-id"),
    path("institute-pricing", InstitutePricing.as_view(), name="institute-pricing"),
    #
    path("freelance-overview", FreelanceOverview.as_view(), name="institute-overview"),
    path("freelance", Freelance.as_view(), name="institute"),
    path("freelance-full", FreelanceFull.as_view(), name="freelance-full"),
    path("freelance-student", FreelanceStudent.as_view(), name="institute-student"),
    path("freelance-student-item/<int:id>", FreelanceStudentItem.as_view(), name="freelance-student-item"),
    path("freelance-student-multiple", FreelanceStudentMultiple.as_view(), name="institute-student-multiple"),
    #
    path("marketer-overview", MarketerOverview.as_view(), name="marketer-overview"),
    path("marketer-full", MarketerFull.as_view(), name="marketer-full"),
    path("marketers", Marketers.as_view(), name="marketers"),
    #
    path("institute-lists", InstituteLists.as_view(), name="institute-lists"),
    path("student-lists", StudentLists.as_view(), name="student-lists"),
    path("freelance-lists", FreelanceLists.as_view(), name="freelance-lists"),
    #
    path("visit", VisitList.as_view(), name="visit"),
]
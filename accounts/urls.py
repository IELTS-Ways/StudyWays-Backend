from django.urls import path
from accounts.views import Logout,Profile,Refresh,RefreshAccess,OverView,SendOTP,VerifyOTP,EmailSendOTP,\
    UserValidationView, VerifyAndUpdatePhoneNumber, SendUpdateOTP, VerifyEmailOTP, SendEmailOTP, EmailVerifyOTP
from accounts.student_views import StudentLogin,StudentOverview,StudentInstituteData,StudentFull,StudentWalletView
from accounts.institute_views import InstituteOverview,Institute,InstituteStudent,ZarinpalMerchantID,InstituteFull,\
    InstituteStudentMultiple,InstituteStudentItem,InstitutePricing, InstituteWalletView
from accounts.freelance_views import FreelanceOverview,Freelance,FreelanceStudent,FreelanceFull,FreelanceStudentMultiple,\
    FreelanceStudentItem, FreelanceWalletView
from accounts.management_panel_view import InstituteLists,StudentLists,FreelanceLists
from accounts.visitors_views import InstituteLists as VisitList
from accounts.management_panel_view import InstituteLists,StudentLists,FreelanceLists
from accounts.marketer_views import MarketerOverview,MarketerFull,Marketers,MarketerWalletView


urlpatterns = [
    path("otp", SendOTP.as_view(), name="send_otp"),
    path("otp/verify", VerifyOTP.as_view(), name="verify_otp"),
    path("email-otp", EmailSendOTP.as_view(), name="email-otp"),
    path("otp/email-verify", EmailVerifyOTP.as_view(), name="email-verify_otp"),
    path("refresh", Refresh.as_view(), name="refresh"),
    path("refresh-access", RefreshAccess.as_view(), name="refresh-access"),
    path("logout", Logout.as_view(), name="logout"),
    path("profile", Profile.as_view(), name="profile"),
    path("overview", OverView.as_view(), name="overview"),
    path("is-valid", UserValidationView.as_view(), name="is-valid"),
    #
    path("otp/update", SendUpdateOTP.as_view(), name="update-otp"),
    path("otp/update-phone-number", VerifyAndUpdatePhoneNumber.as_view(), name="update-phone-number"),
    # 
    path('otp/send_email_otp', SendEmailOTP.as_view(), name='send_email_otp'),
    path('otp/verify_email_otp', VerifyEmailOTP.as_view(), name='verify_email_otp'),
    # 
    path("student-login", StudentLogin.as_view(), name="student-login"),
    path("student-overview", StudentOverview.as_view(), name="student-overview"),
    path("student-institute-data", StudentInstituteData.as_view(), name="student-institute-data"),
    path("student-full", StudentFull.as_view(), name="student-full"),
    path("student-wallet", StudentWalletView.as_view(), name="student-wallet"),
    #
    path("institute-overview", InstituteOverview.as_view(), name="institute-overview"),
    path("institute", Institute.as_view(), name="institute"),
    path("institute-full", InstituteFull.as_view(), name="institute-full"),
    path("institute-student", InstituteStudent.as_view(), name="institute-student"),
    path("institute-student-item/<int:id>", InstituteStudentItem.as_view(), name="institute-student-item"),
    path("institute-student-multiple", InstituteStudentMultiple.as_view(), name="institute-student-multiple"),
    path("zp-id", ZarinpalMerchantID.as_view(), name="zp-id"),
    path("institute-pricing", InstitutePricing.as_view(), name="institute-pricing"),
    path("institute-wallet", InstituteWalletView.as_view(), name="institute-wallet"),
    #
    path("freelance-overview", FreelanceOverview.as_view(), name="institute-overview"),
    path("freelance", Freelance.as_view(), name="freelance"),
    path("freelance-full", FreelanceFull.as_view(), name="freelance-full"),
    path("freelance-student", FreelanceStudent.as_view(), name="freelance-student"),
    path("freelance-student-item/<int:id>", FreelanceStudentItem.as_view(), name="freelance-student-item"),
    path("freelance-student-multiple", FreelanceStudentMultiple.as_view(), name="freelance-student-multiple"),
    path("freelance-wallet", FreelanceWalletView.as_view(), name="freelance-wallet"),
    #
    path("marketer-overview", MarketerOverview.as_view(), name="marketer-overview"),
    path("marketer-full", MarketerFull.as_view(), name="marketer-full"),
    path("marketers", Marketers.as_view(), name="marketers"),
    path("marketer-wallet", MarketerWalletView.as_view(), name="marketer-wallet"),
    #
    path("institute-lists", InstituteLists.as_view(), name="institute-lists"),
    path("student-lists", StudentLists.as_view(), name="student-lists"),
    path("freelance-lists", FreelanceLists.as_view(), name="freelance-lists"),
    #
    path("visit", VisitList.as_view(), name="visit"),
]
from django.urls import path
from subscription.views import StudentSubs, AddSub, AddSubPay, SubPayVerify, Membership


urlpatterns = [
    path("student-subs", StudentSubs.as_view(), name="student-subs"),
    path("add-sub", AddSub.as_view(), name="add-sub"),
    path("add-sub-pay", AddSubPay.as_view(), name="add-sub-pay"),
    path("pay-verify/<int:id>/",SubPayVerify.as_view(),name="pay-verify"),
    #
    path("membership-time", Membership.as_view(), name="membership-time"),
]


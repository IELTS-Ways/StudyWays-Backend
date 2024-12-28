from django.urls import path
from subscription.views import StudentSubs, AddSub, AddSubPay, SubPayVerify, Membership, WithdrawRequest, BOGOVerify, BOGOSubPay, ActivateFreeTrialView
from subscription.transactions import FreelanceTransactions, MarketerTransactions,InstituteTransactions, StudentTransactions


urlpatterns = [
    path("student-subs", StudentSubs.as_view(), name="student-subs"),
    path("add-sub", AddSub.as_view(), name="add-sub"),
    path("add-sub-pay", AddSubPay.as_view(), name="add-sub-pay"),
    path("pay-verify/<int:id>/",SubPayVerify.as_view(),name="pay-verify"),
    # 
    path("BOGO-pay", BOGOSubPay.as_view(), name="BOGO-pay"),
    path("BOGO-verify/<int:id>/",BOGOVerify.as_view(),name="BOGO-verify"),
    # 
    path("free-trial",ActivateFreeTrialView.as_view(),name="free-trial"),
    #
    path("membership-time", Membership.as_view(), name="membership-time"),
    #
    path("freelance-transactions", FreelanceTransactions.as_view(), name="freelance-transactions"),
    path("marketer-transactions", MarketerTransactions.as_view(), name="marketer-transactions"),
    # 
    path("institute-transactions", InstituteTransactions.as_view(), name="institute-transactions"),
    # 
    path("student-transactions", StudentTransactions.as_view(), name="student-transactions"),
    # 
    path("withdraw", WithdrawRequest.as_view(), name="withdraw"),
]

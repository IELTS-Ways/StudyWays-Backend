from django.urls import path
from subscription.views import StudentSubs, AddSub, AddSubPay, SubPayVerify, Membership, WithdrawRequest, BOGOVerify, BOGOSubPay, ActivateFreeTrialView, AddGiftSub, AddGiftSubPay
from subscription.transactions import FreelanceTransactions, MarketerTransactions,InstituteTransactions, StudentTransactions
from subscription.discount import Discount, DiscountItem
from subscription.wallet_pay import CheckWallet, CheckWalletAndPay, WalletAndBOGOPay

urlpatterns = [
    path("student-subs", StudentSubs.as_view(), name="student-subs"),
    path("add-sub", AddSub.as_view(), name="add-sub"),
    path("add-sub-pay", AddSubPay.as_view(), name="add-sub-pay"),
    path("pay-verify/<int:id>/",SubPayVerify.as_view(),name="pay-verify"),
    # 
    path("add-gift-sub", AddGiftSub.as_view(), name="add-gift-sub"),
    path("add-gift-sub-pay", AddGiftSubPay.as_view(), name="add-gift-sub-pay"),
    # 
    path("BOGO-pay", BOGOSubPay.as_view(), name="BOGO-pay"),
    path("BOGO-verify/<int:id>/",BOGOVerify.as_view(),name="BOGO-verify"),
    # new ----
    path("check-wallet", CheckWallet.as_view(), name="check-wallet"),
    path("check-wallet-pay", CheckWalletAndPay.as_view(), name="check-wallet-pay"),
    path("wallet-bogo-pay", WalletAndBOGOPay.as_view(), name="wallet-bogo-pay"),
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
    # 
    path("discount-code", Discount.as_view(), name="discount-code"),
    path("discount-code-item/<str:code>", DiscountItem.as_view(), name="discount-code-item"),
]

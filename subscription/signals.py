from django.db.models.signals import post_save
from django.dispatch import receiver
from subscription.models import Withdraw
from accounts.models.marketer_panel import MarketerWallet
from accounts.models.freelance_profile import FreelanceWallet

@receiver(post_save, sender=Withdraw)
def update_wallet_balance(sender, instance, **kwargs):
    if instance.status == 'Paid':
        user = instance.user

        if user.user_type == 'marketer':
            wallet = MarketerWallet.objects.get(user__user=user)
        # elif user.user_type == 'student':
            # pass
        elif user.user_type == 'freelance':
            wallet = FreelanceWallet.objects.get(user__user=user)
        else:
            raise ValueError("Invalid user type.")

        if wallet.balance >= instance.price:
            wallet.balance -= instance.price
            wallet.save()
        else:
            raise ValueError("Insufficient balance in the wallet.")

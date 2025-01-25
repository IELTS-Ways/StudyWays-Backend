from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User, StudentProfile, InstituteProfile, FreelanceProfile, MarketerPanel,FreelanceWallet, MarketerWallet, InstituteWallet, StudentWallet


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if instance.user_type == "student":
        profile, _ = StudentProfile.objects.get_or_create(user=instance)
        if hasattr(instance, 'studentprofile'):
            instance.studentprofile.save()
        StudentWallet.objects.get_or_create(user=profile)

    elif instance.user_type == "institute":
        profile, _ = InstituteProfile.objects.get_or_create(user=instance)
        if hasattr(instance, 'instituteprofile'):
            instance.instituteprofile.save()
        InstituteWallet.objects.get_or_create(user=profile)

    elif instance.user_type == "freelance":
        profile, _ = FreelanceProfile.objects.get_or_create(user=instance)
        if hasattr(instance, 'freelanceprofile'):
            instance.freelanceprofile.save()
        FreelanceWallet.objects.get_or_create(user=profile)

    elif instance.user_type == "marketer":
        profile, _ = MarketerPanel.objects.get_or_create(user=instance)
        if hasattr(instance, 'MarketerPanel'):
            instance.MarketerPanel.save()
        MarketerWallet.objects.get_or_create(user=profile)
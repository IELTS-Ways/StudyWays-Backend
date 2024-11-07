from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User, StudentProfile, InstituteProfile, FreelanceProfile, MarketerPanel


@receiver(post_save, sender=User)
def create_user_profiles(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == "student":
            StudentProfile.objects.get_or_create(user=instance)
        elif instance.user_type == "institute":
            InstituteProfile.objects.get_or_create(user=instance)
        elif instance.user_type == "freelance":
            FreelanceProfile.objects.get_or_create(user=instance)
        elif instance.user_type == "marketer":
            MarketerPanel.objects.get_or_create(user=instance)

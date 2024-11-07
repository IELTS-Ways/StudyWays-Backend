from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User, StudentProfile, InstituteProfile, FreelanceProfile, MarketerPanel

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if instance.user_type == "student":
        StudentProfile.objects.get_or_create(user=instance)
        if hasattr(instance, 'studentprofile'):
            instance.studentprofile.save()
    elif instance.user_type == "institute":
        InstituteProfile.objects.get_or_create(user=instance)
        if hasattr(instance, 'instituteprofile'):
            instance.instituteprofile.save()
    elif instance.user_type == "freelance":
        FreelanceProfile.objects.get_or_create(user=instance)
        if hasattr(instance, 'freelanceprofile'):
            instance.freelanceprofile.save()
    elif instance.user_type == "marketer":
        user_models.MarketerPanel.objects.get_or_create(user=instance)
        if hasattr(instance, 'marketerprofile'):
            instance.marketerprofile.save()

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import StudentProfile


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created and instance.user_type == "student":
        StudentProfile.objects.create(user=instance)
    else:
        instance.studentprofile.save()

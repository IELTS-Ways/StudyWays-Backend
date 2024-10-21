from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import InstituteProfile, User


class MarketerPanel(models.Model):
    address_type_choices = (
        ("Parents' Home", "Parents' Home"),
        ("Dormitory", "Dormitory"),
        ("Personal Residence", "Personal Residence"), )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    province = models.CharField(max_length=256, blank=True, null=True)
    city = models.CharField(max_length=256, blank=True, null=True)
    address = models.CharField(max_length=256, blank=True, null=True)
    occupancy_type = models.CharField(max_length=100, default="Personal Residence", choices=address_type_choices)
    postal_code = models.CharField(max_length=256, blank=True, null=True)
    description = models.TextField(max_length=4000, blank=True, null=True)
    revenue = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return str(self.user)

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created and instance.user_type == "marketer":
        MarketerPanel.objects.create(user=instance)

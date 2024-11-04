from django.db import models
from accounts.models import StudentProfile, User, FreelanceProfile, InstituteProfile
import datetime
from datetime import datetime as date_time
from django.core.exceptions import ValidationError
from django.db.models import F, ExpressionWrapper, fields, DurationField

class SingletonModel(models.Model):
    class Meta:
        abstract = True
    def save(self, *args, **kwargs):
        if not self.pk and self.__class__.objects.exists():
            raise ValidationError('There can be only one instance of this model.')
        return super(SingletonModel, self).save(*args, **kwargs)



class SubscriptionManager(models.Manager):
    def with_remaining_days(self):
        today = date_time.now().date()
        elapsed_days = (today - self.created_at).days
        remaining_expr = ExpressionWrapper(self.day_period - elapsed_days,output_field=fields.IntegerField())
        return self.get_queryset().annotate(remaining_days=remaining_expr)



class Subscription(models.Model):
    status_choices = (
        ("Active", "Active"),
        ("Expired", "Expired"),
        ("Canceled", "Canceled"),)

    type_choices = (
        ("Audio-Video-Scripter", "Audio-Video-Scripter"),
        ("Memory-Mirror", "Memory-Mirror"),
        ("Planner", "Planner"),
        ("Fast-reading", "Fast-reading"),)

    type = models.CharField(max_length=40, choices=type_choices)
    status = models.CharField(max_length=40, default="Active", choices=status_choices)
    user = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    day_period = models.IntegerField(default=0)
    price = models.IntegerField(default=230000)
    created_at = models.DateField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    description = models.CharField(max_length=256, null=True, blank=True)
    freelance = models.ForeignKey(FreelanceProfile, on_delete=models.CASCADE, null=True, blank=True)
    institute = models.ForeignKey(InstituteProfile, on_delete=models.CASCADE, null=True, blank=True)
    ref_id = models.CharField(max_length=256, null=True, blank=True)
    authority = models.CharField(max_length=256, null=True, blank=True)

    objects = SubscriptionManager()

    def expired(self):
        delta = datetime.date.today() - self.created_at
        if delta.days > self.day_period:
            return True
        else:
            return False

    def remaining_days(self):
        today = date_time.now().date()
        elapsed_days = (today - self.created_at).days
        remaining_days = self.day_period - elapsed_days
        if remaining_days <= 0:
            self.status = "Expired"
            self.save()
        return remaining_days

    def __str__(self):
        return str(self.user) +'-'+ str(self.type)





class DefaultPrice(SingletonModel):
    ZP_MERCHANT_ID = models.CharField(max_length=256,default="00000000-0000-0000-0000-000000000000",blank=True,null=True)
    audio_video_scripter = models.IntegerField(blank=True, null=True)
    memory_mirror = models.IntegerField(blank=True, null=True)
    planner = models.IntegerField(blank=True, null=True)
    fast_reading = models.IntegerField(blank=True, null=True)
    apportionment_percentage = models.DecimalField(max_digits=30, decimal_places=1, blank=True, null=True)
    shaba_number = models.CharField(max_length=256,blank=True,null=True)
    def __str__(self):
        return str(self.audio_video_scripter) +" | "+ str(self.memory_mirror)

from django.db import models
from accounts.models import StudentProfile, User, FreelanceProfile, InstituteProfile
import datetime
from datetime import datetime as date_time


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
    day_period = models.IntegerField(default=45)
    price = models.IntegerField(default=230000)
    created_at = models.DateField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    description = models.CharField(max_length=256, null=True, blank=True)
    freelance = models.ForeignKey(FreelanceProfile, on_delete=models.CASCADE, null=True, blank=True)
    institute = models.ForeignKey(InstituteProfile, on_delete=models.CASCADE, null=True, blank=True)
    ref_id = models.CharField(max_length=256, null=True, blank=True)
    authority = models.CharField(max_length=256, null=True, blank=True)

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
        return remaining_days

    def __str__(self):
        return str(self.user) +'-'+ str(self.type)



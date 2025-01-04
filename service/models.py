from django.db import models
from accounts.models import StudentProfile, User
import datetime
from file.models import File
import shortuuid


class Service(models.Model):
    type_choices = (
        ("Audio-Video-Scripter", "Audio-Video-Scripter"),
        ("Memory-Mirror", "Memory-Mirror"),
        ("Planner", "Planner"),
        ("Fast-reading", "Fast-reading"),)
    type = models.CharField(max_length=30, choices=type_choices)
    user = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    text = models.TextField(max_length=10000, null=True, blank=True)
    done = models.BooleanField(default=False)
    start_time = models.CharField(max_length=100, null=True, blank=True)
    end_time = models.CharField(max_length=100, null=True, blank=True)
    duration = models.CharField(max_length=100, null=True, blank=True)
    share_with = models.CharField(max_length=100, null=True, blank=True)
    word_count = models.IntegerField(default=0)
    slash_count = models.IntegerField(default=0)
    average = models.DecimalField(decimal_places=2,max_digits=10, null=True, blank=True)
    playback = models.BooleanField(default=False)
    lock = models.BooleanField(default=False)
    missing_words = models.IntegerField(default=0)
    device = models.CharField(max_length=100, default="unknown")
    created_at = models.DateTimeField(auto_now_add=True)
    full_result = models.JSONField(null=True, blank=True)

    def __str__(self):
        return str(self.user) +'-'+ str(self.type)


class DraftService(models.Model):
    type_choices = (
        ("Audio-Video-Scripter", "Audio-Video-Scripter"),
        ("Memory-Mirror", "Memory-Mirror"),
        ("Planner", "Planner"),
        ("Fast-reading", "Fast-reading"),)
    type = models.CharField(max_length=30, choices=type_choices)
    user = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    text = models.TextField(max_length=10000, null=True, blank=True)
    done = models.BooleanField(default=False)
    start_time = models.CharField(max_length=100, null=True, blank=True)
    end_time = models.CharField(max_length=100, null=True, blank=True)
    duration = models.CharField(max_length=100, null=True, blank=True)
    share_with = models.CharField(max_length=100, null=True, blank=True)
    word_count = models.IntegerField(default=0)
    slash_count = models.IntegerField(default=0)
    average = models.DecimalField(decimal_places=2,max_digits=10, null=True, blank=True)
    playback = models.BooleanField(default=False)
    lock = models.BooleanField(default=False)
    missing_words = models.IntegerField(default=0)
    device = models.CharField(max_length=100, default="unknown")
    created_at = models.DateTimeField(auto_now_add=True)
    full_result = models.JSONField(null=True, blank=True)

    def __str__(self):
        return str(self.user) +'-'+ str(self.type)


class MultipleSpellings(models.Model):
    UK = models.CharField(max_length=70, null=True, blank=True)
    US = models.CharField(max_length=70, null=True, blank=True)
    def __str__(self):
        return str(self.UK) +' | '+ str(self.US)



class HyphenatedAdjectives(models.Model):
    US = models.CharField(max_length=80, null=True, blank=True)
    UK = models.CharField(max_length=80, null=True, blank=True)
    def __str__(self):
        return str(self.US)


class FeedbackSystem(models.Model):
    user = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    star = models.IntegerField(default=0)
    comment = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.star)+" "+str(self.user)
    
    
    
class ReportSharing(models.Model):
    ACCESS_CHOICES = [
        ('allow_any', 'Allow Any'),
        ('is_authenticated', 'Is Authenticated'),
        ('just_parent', 'Just Parent'),
    ]

    user = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    report = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='shared_links')
    access_type = models.CharField(max_length=50, choices=ACCESS_CHOICES)
    link = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_dynamic_link(self, *args, **kwargs):
        if not self.link:
            self.link = shortuuid.ShortUUID().random(length=8)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"ReportSharing(link={self.link}, user={self.user})"
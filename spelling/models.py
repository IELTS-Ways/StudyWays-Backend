from django.db import models
from accounts.models import StudentProfile



class SpellingDrills(models.Model):
    user = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    words = models.CharField(null=True, blank=True, max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.words

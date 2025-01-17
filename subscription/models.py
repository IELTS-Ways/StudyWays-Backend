from django.db import models
from accounts.models import StudentProfile, User, FreelanceProfile, InstituteProfile
import datetime
from datetime import datetime as date_time
from django.core.exceptions import ValidationError
from django.utils.timezone import now, timedelta



class SingletonModel(models.Model):
    class Meta:
        abstract = True
    def save(self, *args, **kwargs):
        if not self.pk and self.__class__.objects.exists():
            raise ValidationError('There can be only one instance of this model.')
        return super(SingletonModel, self).save(*args, **kwargs)




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
    price = models.DecimalField(max_digits=150, decimal_places=4)
    created_at = models.DateField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    description = models.CharField(max_length=256, null=True, blank=True)
    freelance = models.ForeignKey(FreelanceProfile, on_delete=models.CASCADE, null=True, blank=True)
    institute = models.ForeignKey(InstituteProfile, on_delete=models.CASCADE, null=True, blank=True)
    ref_id = models.CharField(max_length=256, null=True, blank=True)
    authority = models.CharField(max_length=256, null=True, blank=True)
    inviter_sales_percentage = models.DecimalField(max_digits=30, decimal_places=3, blank=True, null=True)
    inviter_price = models.DecimalField(max_digits=30, decimal_places=3, blank=True, null=True)
    apportionment_percentage = models.DecimalField(max_digits=30, decimal_places=3, blank=True, null=True)
    freelance_price = models.DecimalField(max_digits=30, decimal_places=3, blank=True, null=True)
    institute_price = models.DecimalField(max_digits=30, decimal_places=3, blank=True, null=True)
    discount_code = models.CharField(max_length=50, blank=True, null=True)

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



class FreeTrial(models.Model):
    status_choices = (
        ("Active", "Active"),
        ("Expired", "Expired"),
    )
    
    user = models.OneToOneField(StudentProfile, on_delete=models.CASCADE, related_name="free_trial")
    start_date = models.DateField(null=True, blank=True)
    day_period = models.IntegerField(default=7)
    is_active = models.CharField(max_length=40, choices=status_choices, default="Active")

    def activate_free_trial(self):
        self.start_date = now().date()
        self.is_active = "Active"
        self.save()

    def check_expired(self):
        if self.is_active == "Active":
            end_date = self.start_date + timedelta(days=self.day_period)
            if now().date() >= end_date:
                self.is_active = "Expired"
                self.save()

    def remaining_days(self):
        if self.is_active == "Active":
            end_date = self.start_date + timedelta(days=self.day_period)
            remaining = (end_date - now().date()).days
            if remaining <= 0:
                self.is_active = "Expired"
                self.save()
            return max(remaining, 0)
        return 0

    def __str__(self):
        return f"FreeTrial for {self.user} - {self.is_active}"



class DefaultPrice(SingletonModel):
    ZP_MERCHANT_ID = models.CharField(max_length=256,default="00000000-0000-0000-0000-000000000000",blank=True,null=True)
    audio_video_scripter = models.IntegerField(blank=True, null=True)
    memory_mirror = models.IntegerField(blank=True, null=True)
    planner = models.IntegerField(blank=True, null=True)
    fast_reading = models.IntegerField(blank=True, null=True)
    apportionment_percentage = models.DecimalField(max_digits=30, decimal_places=3, blank=True, null=True)
    freelance_apportionment_percentage = models.DecimalField(max_digits=30, decimal_places=3, blank=True, null=True)
    shaba_number = models.CharField(max_length=256,blank=True,null=True)
    def __str__(self):
        return str(self.audio_video_scripter) +" | "+ str(self.memory_mirror)
    


class Withdraw(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('Pending', 'Pending'),         
        ('Paid', 'Paid'),
        ('Cancelled', 'Cancelled'), 
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='New')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    cart_number = models.BigIntegerField(blank=True, null=True)
    shaba = models.CharField(max_length=150, blank=True, null=True)
    price = models.DecimalField(max_digits=100, decimal_places=2)
    description = models.TextField(max_length=1000, blank=True, null=True)
    
    def __str__(self):
        return str(self.user) + '-' + str(self.status) 
    
    
    
class DiscountCode(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Expired', 'Expired'),
    ]
    institute = models.ForeignKey(InstituteProfile, on_delete=models.CASCADE, blank=True, null=True)
    code = models.CharField(max_length=50, unique=True, blank=True, null=True)
    discount_percentage = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    limit_days = models.IntegerField(blank=True, null=True)
    usage_limit = models.IntegerField(blank=True, null=True)
    usage_count = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_active(self):
        current_date = now()
        if self.status == 'Expired':
            return False
        if self.limit_days and current_date > self.created_at + timedelta(days=self.limit_days):
            return False
        if self.usage_limit and self.usage_count >= self.usage_limit:
            return False
        return True

    def use_code(self):
        if self.is_active():
            self.usage_count += 1
            if self.usage_limit and self.usage_count >= self.usage_limit:
                self.status = 'Expired'
            self.save()
            return True
        return False
    
    def days_remaining(self):
        if not self.limit_days:
            return None
        expiration_date = self.created_at + timedelta(days=self.limit_days)
        remaining_days = (expiration_date - now()).days
        return max(0, remaining_days)

    def __str__(self):
        return f"{self.code} ({self.discount_percentage}% off)"
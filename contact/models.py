from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

class Contact(models.Model):
    title = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} : {self.description}'
    
class Application(models.Model):
    
    phone_regex = RegexValidator(
        regex=r"^09\d{9}",
        message="{}\n{}".format(
            _("Phone number must be entered in the format: '09999999999'."),
            _("Up to 11 digits allowed."),
        ),
    )
    
    full_name = models.CharField(max_length=50)
    phone_number = models.CharField(validators=[phone_regex],max_length=11)
    email = models.EmailField(max_length=254)
    location = models.CharField(max_length=250)
    question = models.CharField(max_length=100, blank=True)
    CV = models.FileField(upload_to="media/CV", max_length=100)
    photo = models.ImageField(upload_to="media/Application_profile", height_field=None, width_field=None, max_length=None)

    def __str__(self):
        return self.full_name
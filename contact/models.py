from django.db import models

class Contact(models.Model):
    title = models.CharField(max_length=150, blank=True, null=True)
    name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    description = models.TextField(max_length=3000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} : {self.description}'


class Application(models.Model):   
    full_name = models.CharField(max_length=150, blank=True, null=True)
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    location = models.CharField(max_length=250, blank=True, null=True)
    question = models.CharField(max_length=200, blank=True, null=True)
    CV = models.FileField(upload_to="media/CV", max_length=100, blank=True, null=True)
    photo = models.ImageField(upload_to="media/Application_profile", height_field=None, width_field=None, max_length=None, blank=True, null=True)

    def __str__(self):
        return self.full_name
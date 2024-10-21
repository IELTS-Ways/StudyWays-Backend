from django.db import models

class Contact(models.Model):
    title = models.CharField(max_length=50, blank=False)
    name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=254,blank=False)
    description = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} : {self.description}'

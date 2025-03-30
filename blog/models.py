from django.db import models
from accounts.models import User, InstituteProfile
from ckeditor.fields import RichTextField

class Category(models.Model):
    name = models.CharField(max_length=255,unique=True)

    def __str__(self):
        return str(self.name)


class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(InstituteProfile, on_delete=models.CASCADE)
    cover = models.ImageField(upload_to='media/blog_cover',null=True,blank=True)
    body = RichTextField(blank=False,null=True)
    post_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category,null=True,blank=True,on_delete=models.PROTECT)

    def __str__(self):
        return self.title + ' | ' + str(self.author)
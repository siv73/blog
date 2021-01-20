from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.db.models.lookups import StartsWith
from django.forms import widgets
from django.utils import timezone
from taggit.managers import TaggableManager
from django.urls import reverse
import datetime

from taggit.models import Tag
# Create your models here.

class CustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published').order_by('-publish')


class Post(models.Model):
    objects = CustomManager()
    STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'))
    title = models.CharField(max_length=256) 
    slug = models.SlugField(max_length=264, unique_for_date='publish')
    author = models.ForeignKey(User, related_name='blog_posts',on_delete=models.PROTECT)
    body = models.TextField(max_length=1000)
    publish = models.DateTimeField(default=timezone.now)
    #whenever it is created this value will be considerered!
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("detail", args= [self.publish.year,
                                            self.publish.strftime('%m'),
                                            self.publish.strftime('%d'),
                                            self.slug]   )
    


class Comments(models.Model):
    post = models.ForeignKey(Post,related_name='comments',on_delete=models.PROTECT)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    comments = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"Commented by {self.name} on {self.post}"

    
#users created
    """[summary]
        Siva , siwa48b5
        swathi , siwa48b5

    """

class Maintanence(models.Model):
    under_maintanence = models.BooleanField()
    middle_ware_class = models.CharField( max_length=50)
    middle_ware_app = models.CharField(max_length=50)
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth import models as auth_models
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone
from django_quill.fields import QuillField
# Create your models here.
from mdeditor.fields import MDTextField
import uuid
from collegeHub.validators import validate_pdf, validate_image
from markdownx.models import MarkdownxField

CurrentUser = get_user_model()


class User(auth_models.User, auth_models.PermissionsMixin):

    def __str__(self):
        return "{}".format(self.username)


class UserProfile(models.Model):
    profile_pic = models.ImageField(upload_to="images/", blank=True, null=True, default="images/BlueHead.jpg")
    user = models.OneToOneField(CurrentUser, unique=True, on_delete=models.CASCADE, null=True)
    bio = models.CharField(default="", blank=True, max_length=255)
    # bio_html = models.CharField(editable=False)
    age = models.PositiveSmallIntegerField(default=None, blank=True, null=True)
    phone_number = models.CharField(default="", max_length=50, blank=True, null=True)
    location = models.CharField(default="", blank=True, max_length=255)
    occupation = models.CharField(default="", blank=True, max_length=255)
    github = models.CharField(default="", blank=True, max_length=255)
    facebook = models.CharField(default="", blank=True, max_length=255)
    instagram = models.CharField(default="", blank=True, max_length=255)
    linkedin = models.CharField(default="", blank=True, max_length=255)
    resume = models.FileField(upload_to="files/", blank=True, null=True)
    template_number = models.IntegerField(default=0)
    quote = models.CharField(default="", blank=True, max_length=255)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        # return self.bio
        return self.user.username


class Experiences(models.Model):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, unique=True, null=True, related_name='experience')

    def __str__(self):
        return self.profile.__str__()


class Skill(models.Model):
    name = models.CharField(default='', max_length=30)
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='skill', null=True, blank=True)

    def __str__(self):
        return self.profile.__str__() + ':  ' + self.name


class Section(models.Model):
    name = models.CharField(default='', max_length=30)
    experiences = models.ForeignKey(Experiences, on_delete=models.CASCADE, related_name='section', null=True)

    def __str__(self):
        return self.experiences.__str__() + ':  ' + self.name


class Specific(models.Model):
    position = models.CharField(default='', max_length=50)
    company = models.CharField(default='', max_length=50, blank=True, null=True)
    image = models.ImageField(default='media/right-arrow.png', upload_to='media/', blank=True, null=True)
    description = models.CharField(default='This is what I did', max_length=2000)
    bullet_section = models.CharField(default='Bullet, points, are, great', max_length=200)
    link = models.URLField(default='', blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='specific', null=True)

    def get_bullet_list(self):
        return self.bullet_section.split(', ')

    def __str__(self):
        return self.section.__str__() + ':  ' + self.position


class Education(models.Model):
    image = models.ImageField(default='media/right-arrow.png', upload_to='media/', blank=True, null=True)
    institution = models.CharField(default='', max_length=50, null=True)
    certification_name = models.CharField(default='', max_length=50)
    description = models.CharField(default='', max_length=280)
    month = models.CharField(default='01', max_length=2)
    year = models.CharField(default='9999', max_length=4)
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='education', null=True, blank=True)

    def __str__(self):
        return self.profile.__str__() + ':  ' + self.certification_name


class Event(models.Model):
    user =  models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='scheduling', null=True, blank=True)
    title = models.CharField(max_length=200, blank = True, null = True)
    start_time = models.DateTimeField(u'Starting time', help_text=u'Starting time')
    end_time = models.DateTimeField(u'Final time', help_text=u'Final time')
    notes = models.TextField(u'Textual Notes', help_text=u'Textual Notes', blank=True, null=True)
    is_group = models.BooleanField(default=False, blank=True, null=True)
 
    class Meta:
        ordering = ['-start_time']
        
class Project(models.Model):
    name = models.CharField(default='', max_length=50)
    description = models.CharField(default='This is what I did', max_length=2000)
    image = models.ImageField(default='media/right-arrow.png', upload_to='media/', blank=True, null=True)
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='project', null=True, blank=True)
    month = models.CharField(default='', max_length=2, blank=True, null=True)
    year = models.CharField(default='9999', max_length=4)

    def __str__(self):
        return self.profile.__str__() + ':  ' + self.name

class Post(models.Model):
    title = models.CharField(max_length = 100)
    # content = models.TextField()
    # content = QuillField()
    # content = MDTextField()
    content = MarkdownxField(null=True, blank=True)
    date_posted = models.DateTimeField(default = timezone.now)  
    profile =  models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title
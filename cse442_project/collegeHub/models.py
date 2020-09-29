from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth import models as auth_models
# Create your models here.


CurrentUser = get_user_model()

class User(auth_models.User, auth_models.PermissionsMixin):

    def __str__(self):
        return "@{}".format(self.username)

class UserProfile(models.Model):
    profile_pic = models.ImageField(upload_to="images/", blank=True, null=True, default="images/BlueHead.jpg")
    user = models.OneToOneField(CurrentUser, unique=True, on_delete=models.CASCADE, null=True)
    bio = models.TextField(default="", blank=True)
    bio_html = models.TextField(editable=False)

    location = models.CharField(default="", blank=True, max_length=255)
    occupation = models.CharField(default="", blank=True, max_length=255)
    github = models.CharField(default="", blank=True, max_length=255)
    instagram = models.CharField(default="", blank=True, max_length=255)
    linkedin = models.CharField(default="", blank=True, max_length=255)

    quote = models.CharField(default="", blank=True, max_length=255)

    id = models.AutoField(primary_key=True)

    def __str__(self):
        # return self.bio
        return self.user.username

class Experiences(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


class Section(models.Model):
    name = models.CharField(max_length=255)
    experiences = models.ForeignKey(Experiences, on_delete=models.CASCADE)


class Specific(models.Model):
    image = models.ImageField()
    description = models.CharField(max_length=255)
    bullet_section = models.CharField(max_length=255)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    def get_bullet_list(self):
        return self.bullet_section.split(',')







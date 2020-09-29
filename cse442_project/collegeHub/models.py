from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth import models as auth_models
# Create your models here.

CurrentUser = get_user_model()

class User(auth_models.User, auth_models.PermissionsMixin):

    def __str__(self):
        return "@{}".format(self.username)

class UserProfile(models.Model):
    user = models.OneToOneField(CurrentUser, unique=True, on_delete=models.CASCADE, null=True)
    profile_pic = models.ImageField(upload_to="images/", blank=True, null=True, default="images/BlueHead.jpg")
    bio = models.TextField(default="", blank=True)
    bio_html = models.TextField(editable=False)

    location = models.CharField(default="", blank=True, max_length=255)
    occupation = models.CharField(default="", blank=True, max_length=255)
    github = models.CharField(default="", blank=True, max_length=255)
    instagram = models.CharField(default="", blank=True, max_length=255)
    linkedin = models.CharField(default="", blank=True, max_length=255)

    quote = models.CharField(default="", blank=True, max_length=200)

    id = models.AutoField(primary_key=True)

    def __str__(self):
        # return self.bio
        return self.user.username
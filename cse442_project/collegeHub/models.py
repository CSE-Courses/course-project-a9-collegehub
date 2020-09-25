from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth import models as auth_models
# Create your models here.


CurrentUser = get_user_model()

class User(auth_models.User, auth_models.PermissionsMixin):

    def __str__(self):
        return "@{}".format(self.username)


class Experiences(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Section(models.Model):
    name = models.CharField()
    experiences = models.ForeignKey(Experiences, on_delete=models.CASCADE)


class Specific(models.Model):
    image = models.ImageField()
    description = models.CharField()
    bullet_section = models.CharField()
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    def get_bullet_list(self):
        return self.bullet_section.split(',')







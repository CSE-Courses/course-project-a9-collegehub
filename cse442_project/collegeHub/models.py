from django.db import models

# Create your models here.


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






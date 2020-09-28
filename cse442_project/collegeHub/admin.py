from django.contrib import admin
from collegeHub.models import Section, Specific, Experiences, User

# Register your models here.

admin.site.register(User)
admin.site.register(Experiences)
admin.site.register(Section)
admin.site.register(Specific)

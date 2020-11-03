from __future__ import unicode_literals
from django.contrib import admin
from collegeHub.models import Section, Specific, Experiences, User, UserProfile, Education, Skill, IndividualScheduler
import datetime
import calendar
from django.urls import reverse
from calendar import HTMLCalendar
from django.utils.safestring import mark_safe
# Register your models here.
# admin.site.register(User)
class EventAdmin(admin.ModelAdmin):
    list_display = ['day', 'start_time', 'end_time', 'notes']
 


admin.site.register(Experiences)
admin.site.register(Section)
admin.site.register(Specific)
admin.site.register(UserProfile)
admin.site.register(IndividualScheduler)
admin.site.register(Education)
admin.site.register(Skill)


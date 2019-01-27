from django.contrib import admin

# Register your models here.
from .models import Profile,Student_Profile,Faculty_Profile,Community_Profile

admin.site.register(Profile)
admin.site.register(Student_Profile)
admin.site.register(Faculty_Profile)
admin.site.register(Community_Profile)

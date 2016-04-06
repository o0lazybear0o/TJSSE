from django.contrib import admin

from .models import UserProfile, Credit

admin.site.register(UserProfile)
admin.site.register(Credit)

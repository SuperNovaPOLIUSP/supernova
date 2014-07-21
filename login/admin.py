from django.contrib import admin
from django.contrib.auth.models import User
# Import the UserProfile model individually.
from login.models import UserProfile

admin.site.register(UserProfile)

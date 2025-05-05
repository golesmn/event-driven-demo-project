from django.contrib import admin
from .models.user_management.user import UserProfile
from .models.notification_management.notification import Notification

admin.site.register(UserProfile)
admin.site.register(Notification)
# Register your models here.

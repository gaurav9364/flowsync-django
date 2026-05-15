from django.contrib import admin
from .models import User, Notification, ActivityLog

admin.site.register(User)
admin.site.register(Notification)
admin.site.register(ActivityLog)
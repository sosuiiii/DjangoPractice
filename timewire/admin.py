from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import User, Work, Check

admin.site.register(User, UserAdmin)
admin.site.register(Work)
admin.site.register(Check)
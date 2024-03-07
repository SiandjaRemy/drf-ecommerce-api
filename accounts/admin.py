from django.contrib import admin
from .models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "first_name", "last_name", "is_staff", "is_superuser"]
    # pass

admin.site.register(User, UserAdmin)


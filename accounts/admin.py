from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ["username", "email", "is_staff", "is_active","profile_picture"]  # Customize as needed
    fieldsets = UserAdmin.fieldsets + (  
        ("Additional Info", {"fields": ("bio", "profile_picture")}),  
    )
    add_fieldsets = UserAdmin.add_fieldsets + (  
        ("Additional Info", {"fields": ("bio", "profile_picture")}),  
    )

admin.site.register(CustomUser, CustomUserAdmin) 

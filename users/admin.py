from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import OTP, User, Region, District


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ["name", "region"]
    list_filter = ["region"]


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("first_name", "last_name", "phone", "region", "district", "score", "balance", "study_time", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active", "region", "district")
    fieldsets = (
        (None, {"fields": ("first_name", "last_name", "phone", "password", "avatar", "region", "district")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("User Info", {"fields": ("score", "balance", "study_time")}),
        ("Important dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("first_name", "last_name", "phone", "password1", "password2", "is_staff", "is_active", "region", "district")}),)
    search_fields = ("phone", "first_name", "last_name")
    ordering = ("phone",)
    filter_horizontal = ("groups", "user_permissions")


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ("user", "code", "created_at", "is_available")
    search_fields = ("user__phone", "code")
    list_filter = ("created_at",)

    def is_available(self, obj):
        return not obj.is_expired()

    is_available.boolean = True

from django.contrib import admin

from .models import Payment, Promocode


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "level", "amount", "date", "success")
    search_fields = ("user__username", "level__name")
    list_filter = ("success",)
    ordering = ("-date",)


@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    list_display = ["id", "code", "discount", "created_at", "expires_at"]

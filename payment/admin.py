from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "level", "amount", "date", "success")
    search_fields = ("user__username", "level__name")
    list_filter = ("success",)
    ordering = ("-date",)

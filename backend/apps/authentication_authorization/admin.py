from django.contrib import admin
from .models import AllowedIPRange


@admin.register(AllowedIPRange)
class AllowedIPRangeAdmin(admin.ModelAdmin):
    list_display = ['network', 'description', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['network', 'description']
    ordering = ['-is_active', 'network']

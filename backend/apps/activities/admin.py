from django.contrib import admin
from .models import Activity


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'category']

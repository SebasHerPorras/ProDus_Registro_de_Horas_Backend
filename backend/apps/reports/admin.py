from django.contrib import admin
from .models import DayReported, DayReportHistory


@admin.register(DayReported)
class DayReportedAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'activity', 'date', 'start_time', 'end_time', 'status', 'manager']
    list_filter = ['status', 'date', 'activity']
    search_fields = ['user__username', 'activity__name', 'notes']
    date_hierarchy = 'date'
    readonly_fields = ['last_modified_at', 'created_at']


@admin.register(DayReportHistory)
class DayReportHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'day_report', 'changed_by_user', 'new_status', 'changed_at']
    list_filter = ['new_status', 'changed_at']
    search_fields = ['day_report__user__username', 'changed_by_user__username']
    readonly_fields = ['changed_at']

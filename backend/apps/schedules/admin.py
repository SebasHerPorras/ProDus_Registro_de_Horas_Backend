from django.contrib import admin
from .models import Schedule, ScheduleDay


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['user', 'hours_per_week']
    search_fields = ['user__username']


@admin.register(ScheduleDay)
class ScheduleDayAdmin(admin.ModelAdmin):
    list_display = ['user', 'day_number', 'start_time', 'end_time', 'hours_per_day']
    list_filter = ['day_number']
    search_fields = ['user__username']

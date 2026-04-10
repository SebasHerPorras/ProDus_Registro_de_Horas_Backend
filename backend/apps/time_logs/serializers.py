from rest_framework import serializers
from django.utils import timezone

from apps.time_logs.models import TimeLog


class TimeLogSerializer(serializers.ModelSerializer):
    status_code = serializers.CharField(source='status.code', read_only=True)
    elapsed_seconds = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = TimeLog
        fields = [
            'id',
            'check_in',
            'check_out',
            'status_code',
            'work_description',
            'break_minutes',
            'elapsed_seconds',
            'is_active',
        ]
        read_only_fields = ['check_in', 'status_code']

    def get_elapsed_seconds(self, obj):
        end_moment = obj.check_out or timezone.now()
        return int((end_moment - obj.check_in).total_seconds())

    def get_is_active(self, obj):
        return obj.check_out is None and getattr(obj.status, 'code', None) == 'IN_PROGRESS'
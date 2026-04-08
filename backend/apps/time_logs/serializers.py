from rest_framework import serializers

from apps.time_logs.models import TimeLog


class TimeLogSerializer(serializers.ModelSerializer):
    status_code = serializers.CharField(source='status.code', read_only=True)

    class Meta:
        model = TimeLog
        fields = [
            'check_in',
            'check_out',
            'status_code',
            'work_description',
            'break_minutes',
        ]
        read_only_fields = ['check_in', 'status_code']
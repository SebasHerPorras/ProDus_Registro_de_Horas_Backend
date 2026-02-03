"""
Serializers para el módulo de reportes.
"""
from rest_framework import serializers
from .models import DayReported, DayReportHistory


class DayReportHistorySerializer(serializers.ModelSerializer):
    """
    Serializer para DayReportHistory.
    """
    changed_by_username = serializers.CharField(source='changed_by_user.username', read_only=True)
    activity_name = serializers.CharField(source='activity.name', read_only=True)
    
    class Meta:
        model = DayReportHistory
        fields = [
            'id', 'day_report', 'changed_by_user', 'changed_by_username',
            'activity', 'activity_name', 'new_start_time', 'new_end_time',
            'new_status', 'notes', 'changed_at', 'manager'
        ]
        read_only_fields = ['id', 'changed_at']


class DayReportedSerializer(serializers.ModelSerializer):
    """
    Serializer para DayReported.
    """
    username = serializers.CharField(source='user.username', read_only=True)
    activity_name = serializers.CharField(source='activity.name', read_only=True)
    activity_category = serializers.CharField(source='activity.category', read_only=True)
    hours_worked = serializers.FloatField(read_only=True)
    history = DayReportHistorySerializer(many=True, read_only=True)
    
    class Meta:
        model = DayReported
        fields = [
            'id', 'user', 'username', 'activity', 'activity_name', 'activity_category',
            'start_time', 'end_time', 'date', 'notes', 'status', 'manager',
            'hours_worked', 'last_modified_at', 'created_at', 'history'
        ]
        read_only_fields = ['id', 'last_modified_at', 'created_at', 'hours_worked']


class DayReportedCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para crear reportes diarios.
    """
    class Meta:
        model = DayReported
        fields = ['activity', 'start_time', 'end_time', 'date', 'notes']
    
    def validate(self, data):
        # Validar que end_time sea mayor que start_time
        if data['end_time'] <= data['start_time']:
            raise serializers.ValidationError({
                'end_time': 'La hora de fin debe ser mayor que la hora de inicio.'
            })
        return data
    
    def create(self, validated_data):
        # Asignar el usuario del request
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class DayReportedApprovalSerializer(serializers.Serializer):
    """
    Serializer para aprobar/rechazar reportes.
    """
    status = serializers.ChoiceField(choices=['APPROVED', 'REJECTED'])
    notes = serializers.CharField(required=False, allow_blank=True, max_length=500)


class DayReportedBulkCreateSerializer(serializers.Serializer):
    """
    Serializer para crear múltiples reportes a la vez.
    """
    reports = DayReportedCreateSerializer(many=True)
    
    def create(self, validated_data):
        user = self.context['request'].user
        reports = []
        
        for report_data in validated_data['reports']:
            report_data['user'] = user
            reports.append(DayReported(**report_data))
        
        return DayReported.objects.bulk_create(reports)

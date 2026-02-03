"""
Serializers para el módulo de horarios.
"""
from rest_framework import serializers
from .models import Schedule, ScheduleDay


class ScheduleDaySerializer(serializers.ModelSerializer):
    """
    Serializer para ScheduleDay.
    """
    day_name = serializers.CharField(source='get_day_number_display', read_only=True)
    
    class Meta:
        model = ScheduleDay
        fields = ['id', 'user', 'day_number', 'day_name', 'start_time', 'end_time', 'hours_per_day']
        read_only_fields = ['id']


class ScheduleSerializer(serializers.ModelSerializer):
    """
    Serializer para Schedule con días incluidos.
    """
    username = serializers.CharField(source='user.username', read_only=True)
    schedule_days = ScheduleDaySerializer(source='user.schedule_days', many=True, read_only=True)
    
    class Meta:
        model = Schedule
        fields = ['user_id', 'username', 'hours_per_week', 'schedule_days']


class ScheduleCreateSerializer(serializers.Serializer):
    """
    Serializer para crear horario completo con días.
    """
    user_id = serializers.IntegerField()
    hours_per_week = serializers.IntegerField(min_value=1, max_value=48)
    days = serializers.ListField(
        child=serializers.DictField(),
        required=False
    )
    
    def create(self, validated_data):
        from apps.users.models import User
        from django.db import transaction
        
        days_data = validated_data.pop('days', [])
        user = User.objects.get(id=validated_data['user_id'])
        
        with transaction.atomic():
            schedule, _ = Schedule.objects.update_or_create(
                user=user,
                defaults={'hours_per_week': validated_data['hours_per_week']}
            )
            
            # Eliminar días anteriores y crear nuevos
            ScheduleDay.objects.filter(user=user).delete()
            
            for day_data in days_data:
                ScheduleDay.objects.create(
                    user=user,
                    day_number=day_data['day_number'],
                    start_time=day_data['start_time'],
                    end_time=day_data['end_time'],
                    hours_per_day=day_data.get('hours_per_day', 0)
                )
        
        return schedule

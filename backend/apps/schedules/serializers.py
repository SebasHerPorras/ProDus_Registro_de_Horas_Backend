from rest_framework import serializers
from .models import Schedule, ScheduleBlock
from apps.users.models import Assistant
from .services import ScheduleService

class ScheduleBlockCreateSerializer(serializers.Serializer):
    day_of_week = serializers.ChoiceField(ScheduleBlock.DayOfWeek)
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()

    def validate(self, attrs):
        start_time = attrs.get("start_time")
        end_time = attrs.get("end_time")

        if (start_time > end_time):
            raise serializers.ValidationError({'start_time':'La hora de inicio de un bloque no puede ser mayor a la hora de fin.'})
        
        if (start_time == end_time):
            raise serializers.ValidationError({'end_time': 'El bloque debe tener una duración mayor a 0'})
        return attrs


class ScheduleCreateSerializer(serializers.Serializer):
    assistant = serializers.PrimaryKeyRelatedField(queryset=Assistant.objects.all())
    valid_from = serializers.DateField()
    valid_to = serializers.DateField(required=False, allow_null=True)
    blocks = ScheduleBlockCreateSerializer(many=True)

    def create(self, validated_data):
        return ScheduleService.createAssistantScheduleWithBlocks(**validated_data)
    
class ScheduleBlockDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleBlock
        fields = ['id', 'day_of_week', 'start_time', 'end_time']
        
class ScheduleDetailSerializer(serializers.ModelSerializer):
    blocks = ScheduleBlockDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Schedule
        fields = ['id', 'assistant', 'valid_from', 'valid_to', 'blocks']

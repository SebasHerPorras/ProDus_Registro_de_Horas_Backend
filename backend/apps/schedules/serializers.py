from rest_framework import serializers

class ScheduleBlockCreateSerializer(serializers.Serializer):
    day_of_week = serializers.ChoiceField(ScheduleBlock.DayOfWeek)
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
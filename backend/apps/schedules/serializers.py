from rest_framework import serializers

class ScheduleBlockCreateSerializer(serializers.Serializer):
    day_of_week = serializers.CharField(max_length=15)
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
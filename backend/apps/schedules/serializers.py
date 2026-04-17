from rest_framework import serializers

class ScheduleBlockCreateSerializer(serializers.Serializer):
    day_of_week = serializers.CharField(max_length=15)
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()

class ScheduleCreateSerializer(serializers.Serializer):
    assistant = serializers.IntegerField()
    valid_from = serializers.DateField()
    valid_to = serializers.DateField(required=False, allow_null=True)
    blocks = ScheduleBlockCreateSerializer(many=True)
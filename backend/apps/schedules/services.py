from django.db import transaction
from .models import Schedule, ScheduleBlock

class ScheduleService:
    @staticmethod
    def createSchedule(assistant, valid_from, valid_to=None) -> Schedule:
        schedule = Schedule.objects.create(
            assistant=assistant,
            valid_from=valid_from,
            valid_to=valid_to,
        )

        schedule.save()

        return schedule

    @staticmethod
    @transaction.atomic
    def createScheduleBlocks(schedule, blocks):
        for block_data in blocks:
            block = ScheduleBlock.objects.create(
                schedule=schedule,
                **block_data,
            )

    @staticmethod
    @transaction.atomic
    def createAssistantScheduleWithBlocks(*, assistant, blocks, valid_from, valid_to=None) -> Schedule:
        schedule = ScheduleService.createSchedule(assistant, valid_from, valid_to)
        
        ScheduleService.createScheduleBlocks(schedule, blocks)

        return schedule

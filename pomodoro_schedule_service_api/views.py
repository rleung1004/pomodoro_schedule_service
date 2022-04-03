from django.http import HttpResponse
from pomodoro_schedule_service_api import models
from django.views.decorators.csrf import csrf_exempt

from pomodoro_schedule_service_api.scheduler import Scheduler


@csrf_exempt
def update_schedule(request):
    if request.method == 'POST':
        user_id = request.POST.get("user_id", "")

        # delete old schedule #
        models.Schedule.objects.filter(userId=user_id).delete()

        user_commitments = list(models.Commitment.objects.all())
        user_goals = list(models.Goal.objects.all())
        user_config = list(models.UserConfig.objects.filter(user_id=user_id))
        user_config = dict({
            {day_config.day, {
                "end": day_config.end, "start": day_config.start,
                "breaks": day_config.breaks, "blockSize": day_config.blockSize,
                "interleaves": day_config.interleaves
            }} for day_config in user_config
        })

        priorities = set([goal.priority for goal in user_goals])
        user_goals = {priority: [goal for goal in user_goals if goal.priority == priority] for priority in priorities}
        schedule = Scheduler.create_schedule(goals=user_goals, commitments=user_commitments, weekly_config=user_config)

        for sorted_dict in schedule.values():
            for time, work_block in sorted_dict.items():
                schedule_table = models.Schedule()
                schedule_table.userId = user_id
                schedule_table.date = work_block.date.strftime("%Y-%m-%d"),
                schedule_table.time = str(time)
                schedule_table.name = work_block.name
                schedule_table.minutes = work_block.minutes
                schedule_table.is_goal = work_block.is_goal
                schedule_table.priority = work_block.priority if work_block.priority else -1
                schedule_table.save()

        return HttpResponse(status=201)

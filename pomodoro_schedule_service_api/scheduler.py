from datetime import datetime, timedelta
from sortedcontainers import SortedDict

from pomodoro_schedule_service_api.models import WorkBlock


class Scheduler:
    @staticmethod
    def _add_commitments(schedule: dict, commitments: list, _datetime: datetime) -> SortedDict:
        schedule[_datetime.date()] = SortedDict()
        for commitment in commitments:
            if commitment.end >= _datetime.date() \
                    and commitment.start.time() >= _datetime.time() and \
                    (commitment.start.date() == _datetime.date() or _datetime.weekday() in commitment.repeat):
                start_time = (commitment.start + timedelta(seconds=1)).time() \
                    if commitment.start.time() in schedule[_datetime.date()] else commitment.start.time()
                schedule[_datetime.date()][start_time] = WorkBlock(name=commitment.name,
                                                                   date=datetime.strptime(
                                                                       f"{_datetime.date()} {start_time}",
                                                                       "%Y-%m-%d %H:%M:%S"),
                                                                   minutes=commitment.minutes,
                                                                   is_goal=False,
                                                                   priority=-1, task_id=commitment.id)
        return schedule[_datetime.date()]

    @staticmethod
    def _add_tasks_to_day(day_schedule: SortedDict, sorted_goals: dict, date: datetime.date,
                          start_time: int, end_time: int, block_size: int, breaks: list, interleaves: list):
        commitments = list(day_schedule.values())
        current_time = start_time
        priorities = sorted(list(sorted_goals.keys()))
        interleave_i, break_i, commitment_i = 0, 0, 0

        while sorted_goals and current_time < end_time:
            if commitment_i < len(commitments):
                commitment_work_block = commitments[commitment_i]
                start_minutes = commitment_work_block.date.hour * 60 + commitment_work_block.date.minute
                free_block = start_minutes - current_time
                commitment_i += 1
            else:
                free_block = end_time - current_time

            time_used = 0
            while sorted_goals and free_block > time_used:
                priority = priorities[0]
                goal_list = sorted_goals[priority]

                if len(goal_list) > 0:
                    time_available = free_block - time_used - breaks[break_i]
                    time_available = block_size if time_available > block_size else time_available
                    min_task_time = goal_list[interleave_i].min_task_time
                    time_available = min_task_time if time_available < min_task_time else time_available
                    goal_i = interleave_i if time_available >= min_task_time \
                        else next((i for i, g in enumerate(goal_list) if time_available >= g.min_task_time), -1)

                    if goal_i < 0:
                        time_used += free_block
                        current_time += free_block
                        break

                    else:
                        goal_data = goal_list[goal_i]
                        start_time = \
                            datetime.strptime(f"{int(current_time / 60)}:{int(current_time % 60)}:0", "%H:%M:%S").time()
                        goal_time = min(goal_data.time_left, time_available)
                        day_schedule[start_time] = WorkBlock(name=goal_data.name,
                                                             date=date,
                                                             minutes=goal_time,
                                                             is_goal=True,
                                                             priority=goal_data.priority, task_id=goal_data.id)
                        goal_data.time_left -= goal_time

                        if goal_data.time_left < goal_data.min_task_time:
                            del goal_list[goal_i]

                        current_time += goal_time
                        time_used += goal_time
                        start_time = \
                            datetime.strptime(f"{int(current_time / 60)}:{int(current_time % 60)}:0", "%H:%M:%S").time()
                        day_schedule[start_time] = WorkBlock(name=f"break_{break_i}_{breaks[break_i]}",
                                                             date=date,
                                                             minutes=breaks[break_i],
                                                             is_goal=False,
                                                             priority=-1, task_id="break")
                        current_time += breaks[break_i]
                        time_used += breaks[break_i]
                        break_i = 0 if break_i + 1 >= len(breaks) else break_i + 1
                        interleave_i = 0 if interleave_i + 1 >= min(len(goal_list), interleaves) else interleave_i + 1

                else:
                    del sorted_goals[priority]
                    del priorities[0]

    @staticmethod
    def create_schedule(goals: dict, commitments: list, weekly_config: dict):
        schedule = {}
        current_day = datetime.now()
        goals = {k: [g for g in v if (g.ignoreDeadline or g.end >= current_day.date())
                     and g.time_left >= g.min_task_time] for k, v in goals.items()}
        sorted_goals = {
            k: sorted(list(v), key=lambda goal: (goal.end - current_day.date()).total_seconds() / goal.time_left)
            for k, v in goals.items()}

        while sorted_goals:
            day_config = weekly_config[current_day.weekday()]

            if current_day.date() != datetime.now().date() \
                    or datetime.now().hour * 60 + datetime.now().minute < day_config['start']:
                current_day = current_day.replace(hour=int(day_config['start'] / 60),
                                                  minute=int(day_config['start'] % 60))

                start_time = day_config['start']
            else:
                start_time = current_day.hour * 60 + current_day.minute

            day_schedule = Scheduler._add_commitments(schedule, commitments, current_day)
            Scheduler._add_tasks_to_day(day_schedule=day_schedule, sorted_goals=sorted_goals,
                                        date=current_day.date(),
                                        start_time=start_time,
                                        end_time=day_config['end'],
                                        block_size=day_config['block_size'], breaks=day_config['breaks'],
                                        interleaves=day_config['interleaves'])
            current_day += timedelta(days=1)
        return schedule


if __name__ == '__main__':
    pass

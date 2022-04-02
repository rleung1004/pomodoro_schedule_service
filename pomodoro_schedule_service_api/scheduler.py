from datetime import datetime, timedelta
from sortedcontainers import SortedDict


class Goal:
    def __init__(self, name: str, total_time: int, priority: int, end: datetime.date, ignore_deadline: bool = False,
                 min_task_time: int = 15):
        self.name = name
        self.total_time = total_time  # total time in minutes so 10 hours is 600
        self.time_left = total_time  # also in minutes
        self.priority = priority
        self.end = end
        self.ignore_deadline = ignore_deadline
        self.min_task_time = min_task_time

    def __eq__(self, other):
        return self.name == other.name


class WorkBlock:
    def __init__(self, name: str, date: datetime, minutes: int, is_goal: bool, priority: int = None):
        self.name = name
        self.date = date
        self.minutes = minutes
        self.is_goal = is_goal
        self.priority = priority

    def __lt__(self, other):
        return self.date < other.date


class Commitment:
    def __init__(self, name: str, start: datetime, minutes: int, end: datetime.date, repeat: list = None):
        self.name = name
        self.start = start
        self.minutes = minutes
        self.end = end
        self.repeat = repeat  # list of ints corresponding to which day to repeat (0-6, monday to sunday)


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
                schedule[_datetime.date()][start_time] = WorkBlock(commitment.name,
                                                                   commitment.start,
                                                                   commitment.minutes, False)
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
                    goal_i = interleave_i if time_available > goal_list[interleave_i].min_task_time \
                        else next((i for i, g in enumerate(goal_list) if time_available > g.min_task_time), -1)

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
                                                             priority=goal_data.priority)

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
                                                             priority=-1)

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
        goals = {k: [g for g in v if (g.ignore_deadline or g.end >= current_day.date())
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


def test_schedule_1():
    start_times = [360, 420, 420, 360, 480, 600, 600]
    end_times = [1200, 1200, 1200, 1200, 1200, 1080, 1080]
    breaks = [[10, 30], [10, 30], [10, 30], [10, 30], [10, 30], [60, 120], [60, 120]]
    interleaves = [4, 4, 4, 4, 4, 2, 2]
    block_size = [50, 50, 50, 60, 60, 40, 30]
    week_keys = ["start", "end", "breaks", "interleaves", "block_size"]

    goals_list = [
        Goal(name="Big Data", total_time=1200, priority=0,
             end=datetime.strptime('2022-04-15', "%Y-%m-%d").date(),
             min_task_time=15),
        Goal(name="ML", total_time=1200, priority=0,
             end=datetime.strptime('2022-04-13', "%Y-%m-%d").date(),
             min_task_time=15),
        Goal(name="OS", total_time=1200, priority=0,
             end=datetime.strptime('2022-04-17', "%Y-%m-%d").date(),
             min_task_time=15),
        Goal(name="BLAW", total_time=1200, priority=0,
             end=datetime.strptime('2022-04-18', "%Y-%m-%d").date(),
             min_task_time=15),
        Goal(name="Projects", total_time=600, priority=0,
             end=datetime.strptime('2022-04-8', "%Y-%m-%d").date(),
             min_task_time=15),
        Goal(name="Practice ML", total_time=600, priority=1,
             end=datetime.strptime('2022-12-8', "%Y-%m-%d").date(),
             min_task_time=15)
    ]

    commitments = [
        Commitment(name="Morning Routine",
                   start=datetime.strptime('2022-04-2 8:30:0', "%Y-%m-%d %H:%M:%S"),
                   minutes=30,
                   end=datetime.strptime('2022-10-3 8:30:0', "%Y-%m-%d %H:%M:%S").date(),
                   repeat=[x for x in range(7)]),
        Commitment(name="SCREAM",
                   start=datetime.strptime('2022-04-2 8:30:0', "%Y-%m-%d %H:%M:%S"),
                   minutes=30,
                   end=datetime.strptime('2022-10-3 8:30:0', "%Y-%m-%d %H:%M:%S").date(),
                   repeat=[x for x in range(7)]),
        Commitment(name="Play With Eve",
                   start=datetime.strptime('2022-04-1 13:30:0', "%Y-%m-%d %H:%M:%S"),
                   minutes=45,
                   end=datetime.strptime('2022-10-3 8:30:0', "%Y-%m-%d %H:%M:%S").date(),
                   repeat=[0, 1, 4, 5, 6]),
        Commitment(name="Feed Eve",
                   start=datetime.strptime('2022-04-1 15:30:0', "%Y-%m-%d %H:%M:%S"),
                   minutes=20,
                   end=datetime.strptime('2022-10-3 8:30:0', "%Y-%m-%d %H:%M:%S").date(),
                   repeat=[2]),
        Commitment(name="Eat Lunch",
                   start=datetime.strptime('2022-04-1 12:00:0', "%Y-%m-%d %H:%M:%S"),
                   minutes=20,
                   end=datetime.strptime('2022-10-3 8:30:0', "%Y-%m-%d %H:%M:%S").date(),
                   repeat=[x for x in range(7)]),
        Commitment(name="Eat Dinner",
                   start=datetime.strptime('2022-04-1 18:00:0', "%Y-%m-%d %H:%M:%S"),
                   minutes=20,
                   end=datetime.strptime('2022-10-3 8:30:0', "%Y-%m-%d %H:%M:%S").date(),
                   repeat=[x for x in range(7)])
    ]

    weekly_config = {day: {key: values[i] for i, key in enumerate(week_keys)} for day, values in
                     enumerate(zip(start_times, end_times, breaks, interleaves, block_size))}

    weekly_config_example_structure = {int: {"start": int,
                                             "end": int,
                                             "breaks": [],
                                             "interleaves": int}}
    # Weekly config explanation
    # the int key is the same for the enum of the days of the week (0-6, monday to sunday)
    # the start and end times, I have them as minutes in ints (so like 10am is 600)
    # breaks is list of ints, minutes for each break in the list
    # interleaves is just an int for the number of goals to interlave

    goals = {priority: [goal for goal in goals_list if goal.priority == priority] for priority in range(2)}
    # goals = {int (priority starting from 0, where 0 is highest priority): [goals at that priority]}

    sched = Scheduler.create_schedule(goals=goals, commitments=commitments, weekly_config=weekly_config)
    # Set a debug breakpoint line #235, step one step, then look at the structure of the schedule object after it returns
    print("beans")


if __name__ == '__main__':
    test_schedule_1()

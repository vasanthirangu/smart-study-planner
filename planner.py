import datetime

def create_basic_plan(subjects, exam_date):
    today = datetime.date.today()
    days_left = (exam_date - today).days

    topic_list = []
    for subject, topics in subjects.items():
        for topic in topics:
            topic_list.append(f"{subject} - {topic}")

    per_day = max(1, len(topic_list) // max(1, days_left))

    schedule = []
    index = 0

    for i in range(days_left):
        date = today + datetime.timedelta(days=i)
        tasks = topic_list[index:index+per_day]
        index += per_day

        schedule.append({
            "date": str(date),
            "tasks": tasks
        })

    if index < len(topic_list):
        schedule[-1]["tasks"].extend(topic_list[index:])

    return schedule


def replan_missed_day(schedule):
    if not schedule:
        return schedule

    missed = schedule.pop(0)
    schedule[-1]["tasks"].extend(missed["tasks"])
    return schedule

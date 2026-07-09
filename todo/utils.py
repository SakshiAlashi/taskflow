from django.utils import timezone
from .models import TodayTask,AppState

def get_today_focus_context():

    today_tasks = TodayTask.objects.all().order_by("created_at")

    unfinished_focus_tasks = today_tasks

    today_completed = today_tasks.filter(completed=True).count()

    today_pending = today_tasks.filter(completed=False).count()

    today_total = today_tasks.count()

    if today_total > 0:
        today_progress = int((today_completed / today_total) * 100)
    else:
        today_progress = 0

    if today_progress == 100:
        progress_title = "🎉 Fantastic!"
        progress_message = "You've completed all focus tasks today."

    elif today_progress >= 75:
        progress_title = "🔥 Almost Done"
        progress_message = "Just a little more to finish."

    elif today_progress >= 50:
        progress_title = "😊 Halfway There"
        progress_message = "Keep going, you're making steady progress."

    elif today_progress > 0:
        progress_title = "💪 Great Start!"
        progress_message = "You're off to a good beginning."

    else:
        progress_title = "🚀 Let's Get Started!"
        progress_message = "Add or complete your first focus task."

    return {
        "today_tasks": today_tasks,
        "today_completed": today_completed,
        "today_pending": today_pending,
        "today_progress": today_progress,
        "progress_title": progress_title,
        "progress_message": progress_message,
        "unfinished_focus_tasks": unfinished_focus_tasks,
        "today_total": today_total,
    }


def check_focus_review():

    state, created = AppState.objects.get_or_create(pk=1)

    today = timezone.now().date()

    # New day started
    if state.last_focus_review == today:
        return False
    unfinished = TodayTask.objects.filter(
        completed=False,
        reviewed=False
    ).exists()

    return unfinished

from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, TodayTask,AppState
from django.http import JsonResponse
from django.utils import timezone
import calendar
import json
from datetime import datetime
from .utils import get_today_focus_context,check_focus_review
from .forms import TaskForm , TodayTaskForm

def keep_today_focus(request):

    if request.method == "POST":

        TodayTask.objects.filter(
            completed=False,
            reviewed=False
        ).update(reviewed=True)

        state, _ = AppState.objects.get_or_create(pk=1)
        state.last_focus_review = timezone.now().date()
        state.save()

    return redirect("todo:dashboard")

def task_list(request):
    all_tasks = Task.objects.all().order_by("-created_at")
    task = all_tasks
    status = request.GET.get("status", "all")

    if status == "pending":
        task = task.filter(completed=False)

    elif status == "completed":
        task = task.filter(completed=True)

    elif status == "overdue":
        task = task.filter(completed=False,due_date__lt=timezone.now().date())

    total_count = all_tasks.count()
    overdue_count = all_tasks.filter(completed=False,due_date__lt=timezone.now().date()).count()
    completed_count = all_tasks.filter(completed=True).count()
    pending_count = total_count - completed_count    

    today_focus = get_today_focus_context()
    
    context= {
        'pending_tasks':task.filter(completed=False),
        'completed_tasks':task.filter(completed=True),
        'tasks' : task,

        'total_count': total_count,
        'completed_count':completed_count,
        'pending_count':pending_count,
        "overdue_count": overdue_count,

        'form': TaskForm(),
        'today_form': TodayTaskForm(),

        "show_add_button": True,
        "current_status": status,
    }
    context.update(today_focus)
    return render(request, 'todo/task_list.html', context)

def dashboard(request):
    task = Task.objects.all().order_by('-created_at')
    upcoming_tasks = (Task.objects.filter(completed=False,due_date__gte=timezone.now().date()).order_by("due_date")[:5])
    recent_tasks = Task.objects.order_by("-created_at")[:5]
    total_count = task.count()

    overdue_count = Task.objects.filter(completed=False,due_date__lt=timezone.now().date()).count()
    completed_count = task.filter(completed=True).count()
    pending_count = total_count - completed_count

    overall_progress = 0

    if total_count > 0:
        overall_progress = int((completed_count / total_count) * 100)

    today = timezone.now().date()
    for upcoming_task in upcoming_tasks:

        delta = (upcoming_task.due_date - today).days

        if delta == 0:
            upcoming_task.due_text = "Today"
            upcoming_task.due_class = "due-today"

        elif delta == 1:
            upcoming_task.due_text = "Tomorrow"
            upcoming_task.due_class = "due-tomorrow"

        elif delta > 1 and delta <= 7:
            upcoming_task.due_text = f"{delta} days left"
            upcoming_task.due_class = "due-soon"

        else:
            upcoming_task.due_text = upcoming_task.due_date.strftime("%b %d")
            upcoming_task.due_class = "due-normal"

    today_focus = get_today_focus_context()
    show_focus_review = check_focus_review()
    review_tasks = TodayTask.objects.filter(completed=False,reviewed=False)
    print(recent_tasks)

    context= {
        'pending_tasks':task.filter(completed=False),
        'completed_tasks':task.filter(completed=True),
        'tasks' : task,

        'total_count': total_count,
        'completed_count':completed_count,
        'pending_count':pending_count,
        "overdue_count": overdue_count,
        'overall_progress': overall_progress,

        'form': TaskForm(),
        'today_form': TodayTaskForm(),

        "show_add_button": True,

        'upcoming_tasks': upcoming_tasks,
        "recent_tasks": recent_tasks,
        "show_focus_review": show_focus_review,
        "review_tasks": review_tasks,
    }
    context.update(today_focus)

    return render(request, 'todo/dashboard.html', context)


def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({
                "success": True,
                "message": "Task created successfully."
            })
        
        return JsonResponse({
            "success": False,
            "errors": form.errors
        }, status=400)

# Todays focus  
def today_task_create(request):
    if request.method == "POST":
        form = TodayTaskForm(request.POST)
        if form.is_valid():
            form.save()

    return redirect("todo:dashboard")

def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return JsonResponse({
                "success": True,
                "message": "Task updated successfully."
            })
        
        return JsonResponse({
            "success": False,
            "errors": form.errors
        }, status=400)

    return JsonResponse({"success": False}, status=405)
    
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return JsonResponse({
            "success": True,
            "message": "Task deleted successfully."
        })

    return JsonResponse({"success": False}, status=405)

def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.completed = not task.completed
        task.save()
    return redirect('todo:task_list')

def today_task_toggle(request, pk):
    today_task = get_object_or_404(TodayTask, pk=pk)

    if request.method=="POST":
        today_task.completed = not today_task.completed
        today_task.save()

    return redirect("todo:dashboard")

def focus_review(request):

    if request.method == "POST":

        selected_ids = request.POST.getlist("selected_tasks")

        # Remove every unfinished task that was NOT selected
        TodayTask.objects.filter(completed=False,reviewed=False).exclude(id__in=selected_ids).delete()

        # Mark the selected tasks as reviewed
        TodayTask.objects.filter(id__in=selected_ids).update(reviewed=True)

        # Remove all completed tasks from yesterday
        TodayTask.objects.filter(completed=True).delete()
        
        state, _ = AppState.objects.get_or_create(pk=1)
        state.last_focus_review = timezone.now().date()
        state.save()

    return redirect("todo:dashboard")
from django.utils import timezone
import calendar


def calendar_view(request):

    today = timezone.localdate()

    year = today.year
    month = today.month
    tasks = Task.objects.filter(due_date__year=year,due_date__month=month)

    tasks_by_day = {}

    for task in tasks:
        day = task.due_date.day

        if day not in tasks_by_day:
            tasks_by_day[day] = []

        tasks_by_day[day].append(task)
    
    cal = calendar.monthcalendar(year, month)
    task_json = {}

    for day, tasks in tasks_by_day.items():
        task_json[day] = [
            {
                "title": task.title,
                "priority": task.priority,
                "completed": task.completed,
            }
            for task in tasks
        ]

    context = {
        "calendar": cal,
        "month_name": calendar.month_name[month],
        "year": year,

        "today_day": today.day,
        "current_month": today.month,
        "current_year": today.year,
        
        "tasks": tasks,
        "task_map": tasks_by_day,
        "today": today,
        "task_json": json.dumps(task_json),
    }

    return render(request, "todo/calendar.html", context)
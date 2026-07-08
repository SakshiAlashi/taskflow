from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, TodayTask
from datetime import date
from django.http import JsonResponse
from django.utils import timezone
from .forms import TaskForm , TodayTaskForm

def task_list(request):
    task = Task.objects.all().order_by('-created_at')
    total_count = task.count()

    overdue_count = Task.objects.filter(completed=False,due_date__lt=timezone.now().date()).count()
    completed_count = task.filter(completed=True).count()
    pending_count = total_count - completed_count

    today_tasks = TodayTask.objects.all().order_by('completed', 'created_at')
    today_completed = today_tasks.filter(completed=True).count()
    today_pending = today_tasks.count() - today_completed


    if today_tasks.count() > 0:
        today_progress = int((today_completed / today_tasks.count()) * 100)
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

        'today_tasks': today_tasks,
        'today_completed': today_completed,
        'today_pending': today_pending,
        'today_progress': today_progress,
        
        'progress_title': progress_title,
        'progress_message': progress_message,

    }

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
            upcoming_task.due_text = task.due_date.strftime("%b %d")
            upcoming_task.due_class = "due-normal"

    today_tasks = TodayTask.objects.all().order_by('completed', 'created_at')
    today_completed = today_tasks.filter(completed=True).count()
    today_pending = today_tasks.count() - today_completed


    if today_tasks.count() > 0:
        today_progress = int((today_completed / today_tasks.count()) * 100)
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

        'today_tasks': today_tasks,
        'today_completed': today_completed,
        'today_pending': today_pending,
        'today_progress': today_progress,
        
        'progress_title': progress_title,
        'progress_message': progress_message,

        'upcoming_tasks': upcoming_tasks,
        "recent_tasks": recent_tasks,
    }

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

    return redirect("todo:task_list")

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
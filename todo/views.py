from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Task, TodayTask
from datetime import date
from .forms import TaskForm , TodayTaskForm

def task_list(request):
    task = Task.objects.all().order_by('-created_at')
    total_count = task.count()
    completed_count = task.filter(completed=True).count()
    pending_count = total_count - completed_count

    today_tasks = TodayTask.objects.all().order_by('created_at')
    today_completed = today_tasks.filter(completed=True).count()
    today_pending = today_tasks.count() - today_completed

    if today_tasks.count() > 0:
        today_progress = int((today_completed / today_tasks.count()) * 100)
    else:
        today_progress = 0


    if today_progress == 0:
        progress_title = "🌱 Start Your Day"
        progress_message = "Complete your first focus task."

    elif today_progress <= 25:
        progress_title = "🚀 Good Start"
        progress_message = "You're building momentum."

    elif today_progress <= 50:
        progress_title = "😊 Halfway There"
        progress_message = "Keep going, you're making steady progress."

    elif today_progress <= 75:
        progress_title = "🔥 Almost Finished"
        progress_message = "Only a few focus tasks left."

    elif today_progress < 100:
        progress_title = "🎯 Final Push"
        progress_message = "You're almost there!"

    else:
        progress_title = "🎉 Fantastic!"
        progress_message = "You've completed all focus tasks today."


    context= {
        'pending_tasks':task.filter(completed=False),
        'completed_tasks':task.filter(completed=True),
        'tasks' : task,

        'total_count': total_count,
        'completed_count':completed_count,
        'pending_count':pending_count,

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


def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('todo:task_list'))
    else:
        form = TaskForm()
    return render("todo:task_list")

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
            return redirect(reverse('todo:task_list'))
    else:
        form = TaskForm(instance=task)
    return render(request, 'todo/task_form.html', {'form': form, 'task': task,'show_add_button': False,})
       
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect(reverse('todo:task_list'))
    return render("todo:task_list")

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

    return redirect("todo:task_list")
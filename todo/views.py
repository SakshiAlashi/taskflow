from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Task
from datetime import date
from .forms import TaskForm

def task_list(request):
    task = Task.objects.all().order_by('-created_at')

    total_count = task.count()
    completed_count = task.filter(completed=True).count()
    pending_count = total_count - completed_count

    context= {
        'pending_tasks':task.filter(completed=False),
        'completed_tasks':task.filter(completed=True),
        'tasks' : task,
        'total_count': total_count,
        'completed_count':completed_count,
        'pending_count':pending_count,
        'form': TaskForm(),
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
    return render(request, 'todo/task_form.html', {'form': form})
      

def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect(reverse('todo:task_list'))
    else:
        form = TaskForm(instance=task)
    return render(request, 'todo/task_form.html', {'form': form, 'task': task})
       
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect(reverse('todo:task_list'))
    return render(request, 'todo/task_confirm_delete.html', {'task': task})

def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.completed = not task.completed
        task.save()
    return redirect('todo:task_list')
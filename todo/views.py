from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Task
from datetime import date

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
    }

    return render(request, 'todo/task_list.html', context)


def task_create(request):
    if request.method == 'POST':
        title = request.POST.get('title','').strip()
        description = request.POST.get('description','').strip()
        priority = request.POST.get('priority', 'medium')
        due_date_raw = request.POST.get('due_date', '').strip()

        due_date = None
        error = None

        if not title:
            error = "Title cannot be empty"
        elif due_date_raw:
            try:
                due_date = date.fromisoformat(due_date_raw)
                if due_date<date.today():
                    error = 'Due date cannot be in the past.'
            except ValueError:
                error = 'Invalid due date format'    
        if error:
            return render(request, 'todo/task_form.html', {'error':error})
        Task.objects.create(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
        )
        return redirect(reverse('todo:task_list'))
    return render(request, 'todo/task_form.html')

def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        completed = request.POST.get('completed') == 'on'
        priority = request.POST.get('priority', 'medium')
        due_date_raw = request.POST.get('due_date', '').strip()

        due_date = None
        error = None

        if not title:
            error = 'Title cannot be empty.'
        elif due_date_raw:
            try:
                due_date = date.fromisoformat(due_date_raw)
                date_changed = due_date != task.due_date
                if date_changed and due_date < date.today():
                    error = 'Due date cannot be in the past.'
            except ValueError:
                error = 'Invalid due date format.'

        if error:
            return render(request, 'todo/task_form.html', {'task': task, 'error': error})

        task.title = title
        task.description = description
        task.completed = completed
        task.priority = priority
        task.due_date = due_date
        task.save()
        return redirect(reverse('todo:task_list'))

    return render(request, 'todo/task_form.html', {'task': task})
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
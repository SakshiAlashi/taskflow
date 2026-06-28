from django.db import models
from datetime import date


class Task(models.Model):
    Priorities =[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=10, choices=Priorities, default='medium')
    due_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title
    
    @property
    def is_overdue(self):
        return self.due_date is not None and self.due_date < date.today() and not self.completed

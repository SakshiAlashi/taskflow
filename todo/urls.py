from django.urls import path
from . import views

app_name = "todo"

urlpatterns = [
    # Dashboard (Home)
    path("", views.dashboard, name="dashboard"),

    # Tasks Page (temporary)
    path("tasks/", views.task_list, name="task_list"),

    # Task CRUD
    path("add/", views.task_create, name="task_create"),
    path("edit/<int:pk>", views.task_update, name="task_update"),
    path("delete/<int:pk>", views.task_delete, name="task_delete"),
    path("toggle/<int:pk>", views.task_toggle, name="task_toggle"),

    # Today's Focus
    path("today/add/", views.today_task_create, name="today_task_create"),
    path("today/toggle/<int:pk>/", views.today_task_toggle, name="today_task_toggle"),

    path("today/review/keep/",views.keep_today_focus,name="keep_today_focus"),
    path("today/review/", views.focus_review, name="focus_review"),

    path("calendar/", views.calendar_view, name="calendar"),
]

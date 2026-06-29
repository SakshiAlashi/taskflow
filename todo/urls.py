from django.urls import path
from . import views
app_name = 'todo'

urlpatterns = [
    path('', views.task_list,name ='task_list'),
    path('add/', views.task_create,name ='task_create'),
    path('edit/<int:pk>', views.task_update,name ='task_update'),
    path('delete/<int:pk>', views.task_delete,name ='task_delete'),
    path('toggle/<int:pk>', views.task_toggle,name ='task_toggle'),
    path("today/add/", views.today_task_create,name="today_task_create"),
    path( "today/toggle/<int:pk>/",views.today_task_toggle,name="today_task_toggle",),
]

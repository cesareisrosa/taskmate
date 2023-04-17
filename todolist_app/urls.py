from todolist_app import views
from django.urls import path


urlpatterns = [
    path('', views.todolist, name='todolist'),
    path('delete/<task_id>', views.delete_task, name='delete_task'),
    path('edit/<task_id>', views.edit_task, name='edit_task'),
    path('check/<task_id>', views.check_task, name='check_task'), 
    ]

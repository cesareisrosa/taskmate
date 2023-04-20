from django.shortcuts import render, redirect
from django.http import HttpResponse
from todolist_app.models import TaskList
from todolist_app.form import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def todolist(request):
    if request.method == "POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.manage = request.user
            instance.save()
        messages.success(request, ("Nova tarefa adicionada!"))
        return redirect('todolist')
    else:      
        all_tasks = TaskList.objects.filter(manage=request.user)
        paginator =Paginator(all_tasks, 5)
        page=request.GET.get('pg')
        all_tasks = paginator.get_page(page)
        return render(request, 'todolist.html', {'all_tasks': all_tasks})

@login_required
def delete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.manage == request.user:
        task.delete()
    else:
        messages.error(request, ("Acesso restrito!"))
    return redirect('todolist')

@login_required
def check_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.manage == request.user:
        if task.done == False:
                task.done = True
                messages.success(request, (task.task + " concluída!"))
        else:
                task.done = False
                messages.success(request, (task.task + " pendente!"))
        task.save()             
    else:
        messages.error(request, ("Acesso resrtito!"))
    
    return redirect('todolist')              
    

@login_required
def edit_task(request, task_id):
    if request.method == "POST":
        task = TaskList.objects.get(pk=task_id)
        form = TaskForm(request.POST or None, instance = task)
        if form.is_valid():
            form.save()
        messages.success(request, ("Tarefa atualizada com sucesso!"))
        return redirect('todolist')
    else:      
        task_obj = TaskList.objects.get(pk=task_id)
        return render(request, 'edit.html', {'task_obj': task_obj})

def index(request):
    context = {
        
        'index_text': "Bem-vindo ao Taskmate",
    }
    return render(request, 'index.html', context)

def contact(request):
    context = {
        
        'contact_text': "Faça seu registro.",
    }
    return render(request, 'contact.html', context)

def about(request):
    context = {
        
        'about_text': "Taskmate é o seu controle de afazeres diários. Facilmente você pode inserir uma nova tarefa, excluí-la, dá-la como concluída ou colocá-la novamente como pendente.",
    }
    return render(request, 'about.html', context)
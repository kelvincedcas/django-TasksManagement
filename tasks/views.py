from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else: 
        total_password = 0
        total_password = len(request.POST['password1'])
        if total_password < 8:
            return render(request, 'signup.html', {
                'form': UserCreationForm,
                'error': 'La contraseña debe tener un mínimo de 8 caracteres'
                })
        elif request.POST['password1'] == request.POST['password2']:
            # Register user
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html', {
                'form': UserCreationForm,
                'error': 'El nombre de usuario ya existe'
                })
        else:
            return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Las contraseñas no coinciden'
            })       

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else: 
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrectos'
            })
        else:
            login(request, user)
            return redirect('home')

def signout(request):
    # Crear función para cerrar la sesión existente
    logout(request)
    return redirect('index')

def total_tasks(request):
    pending_tasks = Task.objects.filter(user_id=request.user, datecompleted__isnull=True)
    total_task = pending_tasks.count()
    return total_task

def total_tasks_important(request):
    pending_tasks = Task.objects.filter(user_id=request.user, datecompleted__isnull=True, important=True)
    total_tasks_important = pending_tasks.count()
    return total_tasks_important

def total_tasks_all(request):
    tasks = Task.objects.filter(user_id=request.user)
    total_task_all = tasks.count()
    return total_task_all

def completed_tasks(request):
    completed_tasks = Task.objects.filter(user_id=request.user, datecompleted__isnull=False)
    total_task_completed = completed_tasks.count()
    return total_task_completed

@login_required
def home(request):
    return render(request, 'home.html', {
        'total_task': total_tasks(request),
        'total_task_all': total_tasks_all(request),
        'completed_tasks': completed_tasks(request),
        'total_tasks_important': total_tasks_important(request)

    })

@login_required
def tasks(request):
    tasks = Task.objects.filter(user_id=request.user, datecompleted__isnull=True).order_by('-important', '-created')
    tasksCompleted = Task.objects.filter(user_id=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    if request.method == 'GET':
        return render(request, 'tasks.html', {
            'tasks': tasks,
            'tasksCompleted': tasksCompleted,
            'total_task': total_tasks(request),
            'completed_tasks': completed_tasks(request)
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'tasks.html', {
            'tasks': tasks,
            'tasksCompleted': tasksCompleted,
            'total_task': total_tasks(request),
            'completed_tasks': completed_tasks(request),
            'error': 'El nombre de la tarea es obligatorio'
        })

@login_required
def create_task(request):
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request,'tasks.html', {
                    'message': 'Por favor provee datos válidos',
                })

@login_required        
def task_detail(request, idTask):
    tasks = Task.objects.filter(user_id=request.user, datecompleted__isnull=True).order_by('-important', '-created')
    tasksCompleted = Task.objects.filter(user_id=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    task = get_object_or_404(Task, id=idTask, user=request.user)
    return render(request, 'task_detail.html', {
        'task': task,
        'tasks': tasks,
        'tasksCompleted': tasksCompleted,
        'total_task': total_tasks(request),
        'completed_tasks': completed_tasks(request)
    })

@login_required
def task_edit(request, idTask):
    if request.method == 'GET':
        tasks = Task.objects.filter(user_id=request.user, datecompleted__isnull=True).order_by('-important', '-created')
        tasksCompleted = Task.objects.filter(user_id=request.user, datecompleted__isnull=False).order_by('-datecompleted')
        task = get_object_or_404(Task, id=idTask, user=request.user)
        return render(request, 'task_edit.html', {
            'task': task,
            'tasks': tasks,
            'tasksCompleted': tasksCompleted,
            'total_task': total_tasks(request),
            'completed_tasks': completed_tasks(request)
        })
    else:
        try:
            task = get_object_or_404(Task, id=idTask)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect ('tasks')
        except ValueError:
            return render(request, 'task_edit.html', {
            'task': task,
            'error': 'Proporciona datos válidos',
            'total_task': total_tasks(request)
        })

@login_required
def task_complete(request, idTask):
    try:
        task = get_object_or_404(Task, id=idTask, user=request.user)
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')
    except:
        return render(request, 'task.html', {
            'task': task,
            'error': 'No se pudo marcar la tarea como completada',
            'total_task': total_tasks(request)
        })

@login_required
def delete_modal_task(request, idTask):
        tasks = Task.objects.filter(user_id=request.user, datecompleted__isnull=True).order_by('-important', '-created')
        tasksCompleted = Task.objects.filter(user_id=request.user, datecompleted__isnull=False).order_by('-datecompleted')
        task = get_object_or_404(Task, id=idTask, user=request.user)
        return render(request, 'delete_modal.html', {
            'task': task,
            'tasks': tasks,
            'tasksCompleted': tasksCompleted,
            'total_task': total_tasks(request),
            'completed_tasks': completed_tasks(request)
        })

@login_required
def delete_task(request, idTask):
    try:
        task = get_object_or_404(Task, id=idTask, user=request.user)
        task.delete()
        return redirect('tasks')
    except ValueError:
        return render(request, 'delete_modal.html', {
        'task': task,
        'error': 'Proporciona datos válidos',
        'total_task': total_tasks(request)
        })


@login_required
def module_building(request):
    return render(request, 'construction.html', {
        'total_task': total_tasks(request)
    })
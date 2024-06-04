"""
URL configuration for djangocrud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from tasks import views

urlpatterns = [

    path("__reload__/", include("django_browser_reload.urls")),

    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('tasks/', views.tasks, name='tasks'),
    path('', views.create_task, name='create_task'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.signout, name='logout'),
    path('tasks/<int:idTask>', views.task_detail, name='task_detail'),
    path('tasks/edit/<int:idTask>', views.task_edit, name='task_edit'),
    path('tasks/<int:idTask>/complete', views.task_complete, name='task_complete'),
    path('tasks/<int:idTask>/delete', views.delete_modal_task, name='task_modal_delete'),
    path('tasks/<int:idTask>/delete/confirm', views.delete_task, name='task_delete'),
    path('module_under_building', views.module_building, name='module_building')

]

from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *
from .utils import *


def index(request):
    context = {
        'menu': menu,
        'menu_tools': menu_tools,
        'title': 'Главная страница'
    }

    return render(request, 'tasks/main_page.html', context=context)



# class TaskHome(LoginRequiredMixin, DataMixin, ListView):
#     model = Tasks
#     template_name = 'tasks/home.html'
#     context_object_name = 'tasks'
#     #allow_empty = False
#     login_url = reverse_lazy('register')
#     raise_exception = True
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title='Мой кабинет')
#
#         return dict(list(context.items()) + list(c_def.items()))

    # def get_queryset(self):
    #     return

@login_required(login_url='login')
def taskhome(request):
    tasks = Tasks.objects.filter(added_by=request.user)

    context = {
        'tasks': tasks,
        'menu': menu,
        'menu_tools': menu_tools,
        'title': 'Мой кабинет',
        'username': request.user.username,
    }

    return render(request, 'tasks/home.html', context=context)


class ShowTask(DataMixin, ListView):
    model = Tasks
    template_name = 'tasks/task.html'
    slug_url_kwarg = 'task_slug'
    context_object_name = 'tasks'
    allow_empty = False

    def get_user(self, request):
        return request.user

    # def get_queryset(self):
    #     return Tasks.objects.filter()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        c_def = self.get_user_context(title='Задание ' + str(context['tasks']))

        return dict(list(context.items()) + list(c_def.items()))


# def showtasks(request):
#     tasks = Tasks.objects.filter(added_by=request.user)
#
#     context = {
#         'tasks': tasks,
#         'menu': menu,
#         'title': ''
#     }

def contact(request):
    return render(request, 'tasks/contact.html', {'menu': menu, 'menu_tools': menu_tools,})

# @login_required(redirect_field_name='home')
# def addtask(request):
#     if request.method == 'POST':
#     else:
#         form_class = AddTaskForm()
#         return render(request, 'tasks/addtask.html', {'mks': mks})

# class AddTask(LoginRequiredMixin, DataMixin, CreateView):
#     form_class = AddTaskForm
#     template_name = 'tasks/addtask.html'
#     success_url = reverse_lazy('home')
#     login_url = reverse_lazy('register')
#     raise_exception = True
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title='Добавление задания')
#
#         return dict(list(context.items()) + list(c_def.items()))
#
#     def save_model(self, request, obj, form, change):
#         print("aaa")
#         if not obj.pk:
#             # Only set added_by during the first save.
#             obj.added_by = request.user.username
#         super().save_model(request, obj, form, change)


@login_required(redirect_field_name='main_page')
def addtask(request):
    if request.method == 'POST':
        form = AddTaskForm(request.POST)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.added_by = request.user
            temp.save()
            return redirect('home')
    else:
        form = AddTaskForm()

    context = {
        'menu': menu,
        'menu_tools': menu_tools,
        'title': 'Добавление задания',
        'form': form,
    }

    return render(request, 'tasks/addtask.html', context=context)


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'tasks/register.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'tasks/login.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')



def logout_user(request):
    logout(request)
    return redirect('main_page')


def pageNotFound(request, exception):
    return  HttpResponseNotFound('Страница не найдена')



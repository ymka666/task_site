from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, FormView
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


class DeleteMyView(SuccessMessageMixin, DeleteView):
    model = Tasks
    success_url = reverse_lazy('home')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        return super(DeleteMyView, self).delete(request, *args, **kwargs)


@login_required(login_url='login')
def addtask(request):
    if request.method == 'POST':
        form = AddTaskForm(request.POST)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.added_by = request.user
            temp.slug = f'{request.user.username}'
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


@login_required(login_url='login')
def show_task(request, task_slug):
    task = get_object_or_404(Tasks, slug=task_slug)

    if request.method == 'POST':
        form = UpdateTaskForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            task.title = form.title
            task.slug = f'{request.user.username}_{form.title}'
            task.content = form.content
            task.deadline = form.deadline
            task.status = form.status
            task.save()
            return redirect('home')
    else:
        form = UpdateTaskForm()

    context = {
        'menu': menu,
        'menu_tools': menu_tools,
        'title': f'Задание {task.title}',
        'task': task,
    }

    return render(request, 'tasks/task.html', context=context)


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


class UpdatedLoginUser(LoginUser):
    form_class = LoginUserForm

    def form_valid(self, form):
        remember_me = form.cleaned_data['remember_me']  # get remember me data from cleaned_data of form
        if not remember_me:
            self.request.session.set_expiry(0)  # if remember me is
            self.request.session.modified = True
        return super(UpdatedLoginUser, self).form_valid(form)


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'tasks/contact.html'
    success_url = reverse_lazy('main_page')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('main_page')


def logout_user(request):
    logout(request)
    return redirect('main_page')


def pageNotFound(request, exception):
    return HttpResponseNotFound('Страница не найдена')



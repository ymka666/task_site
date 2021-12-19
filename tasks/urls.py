from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='main_page'),
    path('home/', taskhome, name='home'),
    path('contact/', contact, name='contact'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
    path('login/', LoginUser.as_view(), name='login'),
    path('home/addtask/', addtask, name='addtask'),
    path('home/task/<slug:task_slug>/', ShowTask.as_view(), name='task')
]
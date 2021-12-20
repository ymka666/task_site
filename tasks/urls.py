from django.conf.urls import url
from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='main_page'),
    path('home/', taskhome, name='home'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
    path('login/', LoginUser.as_view(), name='login'),
    path('home/addtask/', addtask, name='addtask'),
    path('home/task/<slug:task_slug>/', show_task, name='task'),
    url(r'^delete-entry/(?P<pk>\d+)/$', DeleteMyView.as_view(), name='delete_view'),
]

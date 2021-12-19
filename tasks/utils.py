from .models import *


menu = [{'title': 'Главная', 'url_name': 'main_page'},
        {'title': 'Мой кабинет', 'url_name': 'home'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        ]

menu_tools = [{'title': 'Добавить задание', 'url_name': 'addtask'},
              ]

class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        context['menu_tools'] = menu_tools
        return context

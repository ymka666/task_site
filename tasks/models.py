from django.conf import settings
from django.db import models
from django.urls import reverse
from unidecode import unidecode
from django.template.defaultfilters import slugify


class Tasks(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField(blank=True, verbose_name='Описание')
    deadline = models.TextField(blank=True, verbose_name='Дедлайн')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    status = models.BooleanField(default=False, verbose_name='Статус')
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'
        ordering = ['time_create', ]
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('task', kwargs={'task_slug': self.slug})
    
    def save(self):
        if not self.id:
            newslug = str(self.title)
            self.slug += f'_{slugify(unidecode(newslug))}'
        super(Tasks, self).save()



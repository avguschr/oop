from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    fio = models.CharField(max_length=128, null=False, verbose_name='ФИО')

    def __str__(self):
        return self.username

    class Meta(AbstractUser.Meta):
        pass


class Category(models.Model):
    name = models.CharField(max_length=256, null=False, verbose_name='Название')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name



class Bid(models.Model):
    new = 'new'
    accepted = 'accepted'
    completed = 'completed'
    status_choices = [
        (new, 'Новая'),
        (accepted, 'Принято в работу'),
        (completed, 'Выполнено')
    ]

    name = models.CharField(max_length=128, null=False, verbose_name='Название')
    description = models.TextField(null=False, verbose_name='Описание')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=False, verbose_name='Категория')
    img = models.ImageField(upload_to='static/images/', null=False, max_length=200, verbose_name='Изображение')
    status = models.CharField(max_length=128, choices=status_choices, default=new, verbose_name='Статус')
    author = models.ForeignKey('User', on_delete=models.CASCADE, null=False, verbose_name='Автор')
    date = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Дата', null=False)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return self.name

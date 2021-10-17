from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    fio = models.CharField(max_length=128, null=False, verbose_name='ФИО')

    class Meta(AbstractUser.Meta):
        pass

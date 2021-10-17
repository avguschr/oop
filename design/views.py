from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import *
from .forms import *


class RegisterUserView(CreateView):
    model = User
    template_name = 'auth/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('design:index')
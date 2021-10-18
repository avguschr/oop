from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from .models import *
from .forms import *


def index(request):
    return render(request, 'index.html')


class RegisterUserView(CreateView):
    model = User
    template_name = 'auth/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('design:index')


class LoginUserView(LoginView):
    model = User
    template_name = 'auth/login.html'
    success_url = reverse_lazy('design:index')

    def get_success_url(self):
        return reverse_lazy('design:index')


class LogoutUserView(LoginRequiredMixin, LogoutView):
    model = User
    template_name = 'auth/logout.html'
    success_url = reverse_lazy('design:index')

    def get_success_url(self):
        return reverse_lazy('design:index')


class BidsView(ListView):
    model = Bid
    template_name = 'index.html'
    context_object_name = 'bids'

    def get_queryset(self):
        return Bid.objects.order_by('-date')

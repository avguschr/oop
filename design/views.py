from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from .models import *
from .forms import *


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
        return reverse_lazy('design:profile')


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

    def get_context_data(self, **kwargs):
        context = super(**kwargs).get_context_data(**kwargs)
        context['count'] = Bid.objects.all().filter(status='accepted').count()
        return context

    def get_queryset(self):
        return Bid.objects.order_by('-date')[:4]



class CreateBidView(CreateView, LoginRequiredMixin):
    model = Bid

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreateBidView, self).form_valid(form)

    fields = (
        'name',
        'description',
        'category',
        'img'
    )

    template_name = 'bids/createBid.html'

    def get_success_url(self):
        return reverse_lazy('design:index')


class DeleteBidView(DeleteView):
    model = Bid
    template_name = 'bids/deleteBid.html'

    def get_object(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        bid = Bid.objects.get(pk=pk)
        if bid.status == 'new':
            return bid
        else:
            raise Http404

    def get_success_url(self):
        return reverse_lazy('design:profile')


class ProfileView(ListView):
    model = Bid
    template_name = 'profile.html'
    context_object_name = 'bids'

    def get_user(self, request):
        user = request.user.username
        return user

    def get_queryset(self):
        if not self.request.GET:
            return Bid.objects.order_by('-date')
        else:
            return Bid.objects.filter(status=self.request.GET['status']).order_by('-date')

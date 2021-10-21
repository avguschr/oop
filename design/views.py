from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.edit import DeleteView, UpdateView
from django.views.generic.list import ListView

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


class LogoutUserView(LogoutView):
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

    def get_object(self, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg)
        bid = Bid.objects.get(pk=pk)
        if bid.status == 'new':
            return bid
        else:
            raise PermissionDenied()

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


class AdminView(ListView):
    model = Bid
    template_name = 'admin/admin.html'
    context_object_name = 'bids'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Bid.objects.all().order_by('-date')
        else:
            raise PermissionDenied()


class UpdateBidView(UpdateView):
    model = Bid
    template_name = 'admin/updateBid.html'
    fields = [
        'status',
        'img_design',
        'comment'
    ]
    def post(self, request, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg)
        bid = Bid.objects.get(pk=pk)
        if bid.status == 'accepted':
            request.POST = request.POST.copy()
            request.POST['comment'] = bid.comment
        return super(UpdateBidView, self).post(request, **kwargs)

    def get_object(self, **kwargs):
        if self.request.user.is_superuser:
            pk = self.kwargs.get(self.pk_url_kwarg)
            bid = Bid.objects.get(pk=pk)
            return bid
        else:
            raise PermissionDenied()

    def form_valid(self, form):
        form.instance.author = form.instance.author
        return super(UpdateBidView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('design:admin')


class CreateCategoryView(CreateView):
    model = Category
    template_name = 'admin/createCategory.html'
    fields = (
        'name',
    )

    def get_success_url(self):
        return reverse_lazy('design:category')


class CategoryView(ListView):
    model = Category
    template_name = 'admin/category.html'
    context_object_name = 'categories'



class DeleteCategoryView(DeleteView):
    model = Category
    template_name = 'admin/deleteCategory.html'
    def get_object(self, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg)
        category = Category.objects.get(pk=pk)
        return category

    def get_success_url(self):
        return reverse_lazy('design:category')
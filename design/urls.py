from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from django.contrib.auth.decorators import user_passes_test

app_name = 'design'
urlpatterns = [
    path('', views.BidsView.as_view(), name='index'),
    path('register', views.RegisterUserView.as_view(), name='register'),
    path('login', views.LoginUserView.as_view(), name='login'),
    path('logout', views.LogoutUserView.as_view(), name='logout'),
    path('profile', login_required(views.ProfileView.as_view(), login_url='/design/login'), name='profile'),
    path('createBid', login_required(views.CreateBidView.as_view(), login_url='/design/login'), name='createBid'),
    path('<int:pk>/deleteBid', views.DeleteBidView.as_view(), name='deleteBid'),
    path('admin', views.AdminView.as_view(), name='admin'),
    path('<int:pk>/updateBid', views.UpdateBidView.as_view(), name='updateBid'),
    path('createCategory',
         user_passes_test(lambda u: u.is_superuser, login_url='/design/login')(views.CreateCategoryView.as_view()),
         name='createCategory'),
    path('category',
         user_passes_test(lambda u: u.is_superuser, login_url='/design/login')(views.CategoryView.as_view()),
         name='category'),
    path('<int:pk>/deleteCategory',
         user_passes_test(lambda u: u.is_superuser, login_url='/design/login')(views.DeleteCategoryView.as_view()),
         name='deleteCategory')
]

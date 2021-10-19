from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'design'
urlpatterns = [
    path('index', views.BidsView.as_view(), name='index'),
    path('register', views.RegisterUserView.as_view(), name='register'),
    path('login', views.LoginUserView.as_view(), name='login'),
    path('logout', views.LogoutUserView.as_view(), name='logout'),
    path('profile', login_required(views.ProfileView.as_view(), login_url='/design/login'), name='profile'),
    path('createBid', login_required(views.CreateBidView.as_view(), login_url='/design/login'), name='createBid'),
    path('<int:pk>/deleteBid', views.DeleteBidView.as_view(), name='deleteBid')g
]

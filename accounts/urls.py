from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.UserCreateView.as_view(), name='signup'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('user-detail/', views.UserDetailView.as_view(), name='user-detail'),
    path('account-balance/', views.AccountBalanceView.as_view(), name='account-balance'),
]


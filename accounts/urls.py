from django.urls import path, include
from .views import UserCreateView, UserLoginView, UserDetailView, AccountBalanceView

urlpatterns = [
    path('signup/', UserCreateView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('user-detail/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('account-balance/<int:pk>/', AccountBalanceView.as_view(), name='account-balance'),
]


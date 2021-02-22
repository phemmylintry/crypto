from django.urls import path, include
from .views import TransactionView

urlpatterns = [
    path('submit-transaction/', TransactionView.as_view(), name='submit-transaction'),
    # path('login/', UserLoginView.as_view(), name='login')
]
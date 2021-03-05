from django.urls import path, include
from . import views

urlpatterns = [
    path('submit-transaction/', views.TransactionView.as_view(), name='submit-transaction'),
    path('transaction-list/', views.TransactionListView.as_view(), name='transaction-list'),
]
from django.urls import path
from . import views

app_name = 'balances'

urlpatterns = [
    path('', views.group_balances, name='balances'),
    path('settlements/', views.group_settlements, name='settlements'),
    path('reimburse/', views.record_reimbursement, name='reimburse'),
]

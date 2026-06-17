from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'groups'

router = DefaultRouter()
router.register(r'', views.GroupViewSet, basename='group')

urlpatterns = [
    path('invitations/<str:token>/', views.get_invitation_info, name='invitation-info'),
    path('invitations/<str:token>/join/', views.join_group_by_invitation, name='invitation-join'),
] + router.urls

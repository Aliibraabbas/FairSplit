from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'groups'

router = DefaultRouter()
router.register(r'', views.GroupViewSet, basename='group')

urlpatterns = router.urls

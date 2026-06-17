from rest_framework.routers import DefaultRouter
from . import views

app_name = 'expenses'

router = DefaultRouter()
router.register(r'', views.ExpenseViewSet, basename='expense')

urlpatterns = router.urls

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('api/auth/', include('accounts.urls')),
    path('api/groups/', include('groups.urls')),
    path('api/groups/<int:group_pk>/expenses/', include('expenses.urls')),
    path('api/groups/<int:group_pk>/balances/', include('balances.urls')),
]

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from config import settings
from apps.catalog.views import get_category_attributes

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(
        url_name='schema'
    ), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(
        url_name='schema'
    ), name='redoc-ui'),
    path('admin/get-category-attributes/<int:category_id>/', get_category_attributes),

]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

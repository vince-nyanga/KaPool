from django.urls import path, include

from .routes import router

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('rest-auth/', include('rest_auth.urls')),
]
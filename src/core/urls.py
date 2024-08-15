"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from user.api.serializers import UserTokenObtainPairSerializer
from user.views import UserObtainTokenPairView
from chats import consumers
from chats.routing import websocket_urlpatterns  # Asegúrate de tener esto si usas routing.py


urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/token/', UserObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),    
    path("api-auth/", include("rest_framework.urls")),
    path("api/users/", include("user.api.urls")),
    path("api/chats/", include("chats.urls")),
    re_path(r'^ws/', include(websocket_urlpatterns)),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

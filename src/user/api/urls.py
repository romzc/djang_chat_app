from django.urls import path, include
from rest_framework import routers
from ..views import UserViewSet, GroupViewSet, ProfileViewSet #, UserObtainTokenPairView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'profiles', ProfileViewSet)
# router.register(r'token', UserObtainTokenPairView)

urlpatterns = [
    path("", include(router.urls)),
]

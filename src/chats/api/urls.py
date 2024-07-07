from django.urls import path, include
from rest_framework import routers
from ..views import MessageViewSet, ChatGroupViewSet, ContactViewSet

router = routers.DefaultRouter()
router.register(r'messages', MessageViewSet)
router.register(r'chatgroups', ChatGroupViewSet)
router.register(r'contact', ContactViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

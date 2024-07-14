from django.urls import path, include, re_path
from rest_framework import routers
from .. import consumers
from ..views import MessageViewSet, ChatGroupViewSet, ContactViewSet

router = routers.DefaultRouter()
router.register(r'messages', MessageViewSet)
router.register(r'chatgroups', ChatGroupViewSet)
router.register(r'contacts', ContactViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

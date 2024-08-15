from django.urls import path, include, re_path
from rest_framework import routers
from . import consumers
from .views import (
    ContactListView,
    ContactCreateView,
    # ChatGroupListView,
    # ChatGroupCreateView
)

# router = routers.DefaultRouter()
# router.register(r'messages', MessageViewSet)
# router.register(r'chatgroups', ChatGroupViewSet)
# router.register(r'contacts', ContactViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    path('contacts/', ContactListView.as_view()),
    path('contacts/create/', ContactCreateView.as_view()),
    # path('chats_groups/',ChatGroupListView.as_view()),
    
]

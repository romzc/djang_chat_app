import json
from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework_simplejwt import authentication

from user.api.serializers import UserSerializer
from .api.serializers import ChatGroupSerializer, ContactSerializer, MessageSerializer
from .models import Contact, ChatGroup, Message


# Create your views here.
class MessageViewSet(viewsets.ModelViewSet):
   """
   API endpoint that allows to be viewed or edited messages
   """
   queryset = Message.objects.all().order_by('-timestamp')
   serializer_class = MessageSerializer
   authentication_classes = [authentication.JWTAuthentication]
   permission_classes = [permissions.IsAuthenticated]

   def get_queryset(self):
      # obtener el usario.
      user = self.request
      
      jsnuser = UserSerializer(user.user).data
      print(json.dumps(jsnuser))

      return Message.objects.all().order_by('-timestamp')
   

class ContactViewSet(viewsets.ModelViewSet):
   """
   API endpoint that allows to be viewed or edited contact
   """
   queryset = Contact.objects.all()
   serializer_class = ContactSerializer
   authentication_classes = [authentication.JWTAuthentication]
   permission_classes = [permissions.IsAuthenticated]


class ChatGroupViewSet(viewsets.ModelViewSet):
   """
   API endpoint that allows to be viewed or edited ChatGroup
   """
   queryset = ChatGroup.objects.all().order_by('-created_at')
   authentication_classes = [authentication.JWTAuthentication]
   serializer_class = ChatGroupSerializer
   permission_classes = [permissions.IsAuthenticated]
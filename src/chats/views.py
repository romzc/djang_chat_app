from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from .api.serializers import ChatGroupSerializer, ContactSerializer, MessageSerializer
from .models import Contact, ChatGroup, Message


# Create your views here.
class MessageViewSet(viewsets.ModelViewSet):
   """
   API endpoint that allows to be viewed or edited messages
   """
   queryset = Message.objects.all().order_by('-timestamp')
   serializer_class = MessageSerializer
   authentication_classes = [JWTAuthentication]
   permission_classes = [permissions.IsAuthenticated]

   def create(self, request, *args, **kwargs):
      print("SE ESTA ENVIANDO TAREAS")
      return super().create(request, *args, **kwargs)

   def get_queryset(self):
      # obtener el usario.
      user = self.request.user
      return Message.objects.filter(Q(sender=user) | Q(receiver=user)).order_by('-timestamp')

   

class ContactViewSet(viewsets.ModelViewSet):
   """
   API endpoint that allows to be viewed or edited contact
   """
   queryset = Contact.objects.all()
   serializer_class = ContactSerializer
   authentication_classes = [JWTAuthentication]
   permission_classes = [permissions.IsAuthenticated]

   def get_queryset(self):
      user = self.request.user
      return Contact.objects.filter(user=user)


class ChatGroupViewSet(viewsets.ModelViewSet):
   """
   API endpoint that allows to be viewed or edited ChatGroup
   """
   queryset = ChatGroup.objects.all().order_by('-created_at')
   authentication_classes = [JWTAuthentication]
   serializer_class = ChatGroupSerializer
   permission_classes = [permissions.IsAuthenticated]
from urllib import request
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, response, status
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication
from .api.serializers import ChatGroupSerializer, ContactSerializer, MessageSerializer
from .models import Contact, ChatGroup, Message

""" Existen problemas al momento de crear nuevos mensajes """
# Create your views here.
class MessageViewSet(viewsets.ModelViewSet):
   """
   API endpoint that allows to be viewed or edited messages
   """
   queryset = Message.objects.all().order_by('-timestamp')
   serializer_class = MessageSerializer
   authentication_classes = [JWTAuthentication]
   permission_classes = [permissions.IsAuthenticated]

   def get_queryset(self):
      # obtener el usuario.
      user = self.request.user
      return Message.objects.filter(Q(sender=user) | Q(receiver=user)).order_by('-timestamp')

   def perform_create(self, serializer):
      # Obtener el usuario autenticado
      sender = self.request.user
      # Obtener el receptor del cuerpo de la solicitud
      receiver_data = self.request.data.get('receiver')
      if not receiver_data:
         raise ValidationError({"receiver": "This field is required."})
      try:
         receiver = User.objects.get(id=receiver_data['id'])
      except User.DoesNotExist:
         raise ValidationError({"receiver": "Invalid user ID."})
      #Crear el mensaje con el sender y receiver especificados
      serializer.save(sender=sender, receiver=receiver)
   

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

   """ Add new contact to current user"""
   def perform_create(self, serializer):
      user = self.request.user
      contact_data = self.request.data.get('contact')
      if not contact_data:
         raise ValidationError({"contact": "Invalid user contact"})
      try:
         contact = User.objects.get(id=contact_data['id'])
      except User.DoesNotExist: 
         raise ValidationError
      serializer.save(user=user, contact=contact)


class ChatGroupViewSet(viewsets.ModelViewSet):
   """
   API endpoint that allows to be viewed or edited ChatGroup
   """
   queryset = ChatGroup.objects.all().order_by('-created_at')
   authentication_classes = [JWTAuthentication]
   serializer_class = ChatGroupSerializer
   permission_classes = [permissions.IsAuthenticated]
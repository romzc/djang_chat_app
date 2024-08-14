from urllib import request
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, response, status
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import views 
from rest_framework.mixins import CreateModelMixin, ListModelMixin

from core.middlewares import JWTAuthMiddleware
from .serializers import (
   ChatGroupSerializer, 
   ContactSerializer, 
   MessageCreateSerializer, 
   MessageUpdateSerializer
)
from .models import Contact, ChatGroup, Message


class MessageListView(ListModelMixin, views.APIView):
   """
   API endpoints to list and create views.
   """
   queryset = Message.objects.all().order_by('-timestamp')
   serializer_class = MessageCreateSerializer
   authentication_classes = [JWTAuthentication]
   permission_classes = [permissions.IsAuthenticated]

   def list(self, request, *args, **kwargs):
      user = request.user
      print(user)
      return super().list(request, *args, **kwargs)


class ContactListCreateView(ListCreateAPIView):
   queryset = Contact.objects.all()
   serializer_class = ContactSerializer
   authentication_classes = [JWTAuthentication]
   permission_classes = [permissions.IsAuthenticated]

   def get_queryset(self):
      user = self.request.user
      return Contact.objects.filter(user=user)


class ContactCreateUpdateView(RetrieveUpdateDestroyAPIView):
   pass


class ContactViewSet(viewsets.ModelViewSet):
   """
   API endpoint that allows to be viewed or edited contact
   """
   queryset = Contact.objects.all()
   serializer_class = ContactSerializer
   authentication_classes = [JWTAuthentication]
   permission_classes = [permissions.IsAuthenticated]
  
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
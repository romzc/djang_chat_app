import json
from typing import Dict
from django.contrib.auth.models import User
from django.dispatch import receiver
from rest_framework import serializers
from .models import Message
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from channels.db import database_sync_to_async
from djangochannelsrestframework.mixins import (
   ListModelMixin,
   RetrieveModelMixin,
   PatchModelMixin,
   UpdateModelMixin,
   CreateModelMixin,
   DeleteModelMixin,
)

class MessageConsumer( GenericAsyncAPIConsumer ):

   class UserSerializer(serializers.ModelSerializer):
      class Meta:
        model = User
        fields = ['id', 'username', 'email']

   class InputSerializer(serializers.Serializer):
      receiver = serializers.IntegerField()
      content = serializers.CharField()

   class OutputSerializer(serializers.Serializer):
      receiver = serializers.SerializerMethodField()
      sender = serializers.SerializerMethodField()
      content = serializers.CharField()

      def get_receiver(self, obj):
         return MessageConsumer.UserSerializer(obj.receiver).data
         
      def get_sender(self, obj):
         return MessageConsumer.UserSerializer(obj.sender).data

   
   async def receive(self, text_data=None, bytes_data=None, **kwargs):
     
      user = self.scope['user']

      if user.is_anonymous:
         await self.send(text_data=json.dumps({'error': 'Unauthorized'}))
         return
      
      serializer = self.InputSerializer(data=json.loads(text_data))
      serializer.is_valid(raise_exception=True)

      receiver = await self.get_user_by_id(serializer.data.get('receiver'))

      if receiver is None:
         return await self.send(text_data=json.dumps({'response': 'receiver not found'}))

      # Create, serializer and return new message
      message = await self.create_mesasage(user, receiver, serializer.data.get('content'))
      serialized_message = self.OutputSerializer(message).data
      await self.send(text_data=json.dumps(serialized_message))
   
   
   @database_sync_to_async
   def create_mesasage(self, user, receiver, content):
      message = Message.objects.create(
         sender=user, 
         receiver=receiver, 
         content=content
      )
      return message

   @database_sync_to_async
   def get_user_by_id(self, user_id):
      try:
         return User.objects.get(id=user_id)
      except User.DoesNotExist:
         return None





   

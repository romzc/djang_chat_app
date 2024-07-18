import json
from typing import Dict
from django.contrib.auth.models import User
from django.dispatch import receiver
from .api.serializers import MessageSerializer
from .models import Message
from djangochannelsrestframework.generics import AsyncAPIConsumer
from channels.db import database_sync_to_async
from djangochannelsrestframework.mixins import (
   ListModelMixin,
   RetrieveModelMixin,
   PatchModelMixin,
   UpdateModelMixin,
   CreateModelMixin,
   DeleteModelMixin
)

class MessageConsumer( AsyncAPIConsumer ):

   async def connect(self):
      return await super().connect()

   async def disconnect(self, code):
      return await super().disconnect(code)
   
   async def receive(self, text_data=None, bytes_data=None, **kwargs):
      # Parse the received message
      # response = awaitsuper().receive(text_data, bytes_data, **kwargs)
      # print(response)
      user = self.scope['user']

      if user.is_anonymous:
         await self.send(text_data=json.dumps({'error': 'Unauthorized'}))
         return

      data = json.loads(text_data)
      message = data.get('content', 'No message received')
      receiver_aux = data.get('receiver', None)

      if receiver_aux is None:
         return await self.send(text_data=json.dumps({'response': 'fill information please'}))

      receiver = await self.get_user_by_id(receiver_aux['id'])

      if receiver is None:
         return await self.send(text_data=json.dumps({'response': 'fill information please'}))

      # Crear y guardar el mensaje
      message = await self.create_mesasage(user, receiver, message)

      # Send a simple response
      await self.send(text_data=json.dumps({
         'response': f'Received message from {user.username}: {receiver}'
      }))
   
   
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





   

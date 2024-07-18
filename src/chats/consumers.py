import json
from typing import Dict
from django.contrib.auth.models import User
from .api.serializers import MessageSerializer
from .models import Message
from djangochannelsrestframework.generics import AsyncAPIConsumer
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
      data = json.loads(text_data)
      message = data.get('message', 'No message received')
      # Send a simple response
      await self.send(text_data=json.dumps({
         'response': f'Received message: {message}'
      }))





   

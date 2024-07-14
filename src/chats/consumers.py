from django.contrib.auth.models import User
from .api.serializers import MessageSerializer
from .models import Message
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import (
   ListModelMixin,
   RetrieveModelMixin,
   PatchModelMixin,
   UpdateModelMixin,
   CreateModelMixin,
   DeleteModelMixin
)

class MessageConsumer(
   ListModelMixin,
   RetrieveModelMixin,
   PatchModelMixin,
   UpdateModelMixin,
   CreateModelMixin,
   DeleteModelMixin,
   GenericAsyncAPIConsumer
):
   queryset = Message.objects.all()
   serializer_class = MessageSerializer
from rest_framework import serializers
from ..models import ChatGroup, Message, Contact
from user.api.serializers import UserSerializer
from django.contrib.auth.models import User

class MessageSerializer(serializers.ModelSerializer):

   sender = UserSerializer()
   receiver = UserSerializer()

   class Meta:
      model = Message
      fields = ['sender', 'receiver', 'timestamp', 'content']


class ChatGroupSerializer(serializers.ModelSerializer):
   class Meta:
      model = ChatGroup
      fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):

   contact = UserSerializer()

   class Meta:
      model = Contact
      fields = ['id', 'user', 'contact']
from os import read
from rest_framework import serializers
from ..models import ChatGroup, Message, Contact
from user.api.serializers import UserSerializer
from django.contrib.auth.models import User

class MessageSerializer(serializers.ModelSerializer):
   
   sender = UserSerializer(read_only=True)
   receiver = UserSerializer(read_only=True)

   class Meta:
      model = Message
      fields = ['id', 'sender', 'receiver', 'timestamp', 'content']

   def create(self, validated_data):
      receiver_data = validated_data.pop('receiver')
      receiver = User.objects.get(id=receiver_data.id)
      message = Message.objects.create(receiver=receiver, **validated_data)
      return message


class ChatGroupSerializer(serializers.ModelSerializer):
   class Meta:
      model = ChatGroup
      fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):

   contact = UserSerializer(read_only=True)
   user = UserSerializer(read_only=True)

   class Meta:
      model = Contact
      fields = ['id', 'user', 'contact']



"""

"""
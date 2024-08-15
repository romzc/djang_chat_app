from typing import Iterable
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# Create your models here.
class Contact(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
   contact = models.ForeignKey(User, on_delete=models.CASCADE, related_name='related_to')

   class Meta:
      unique_together = ('user', 'contact')

   def __str__(self) -> str:
      return f"{str(self.user)} - {str(self.contact)}"


class ChatRoom(models.Model):
   group_name = models.CharField(max_length=255, blank=True)
   chat_code = models.CharField(max_length=100, blank=False)
   created_at = models.DateTimeField(auto_now_add=True)
   created_by = models.ForeignKey(User, related_name='created_groups', on_delete=models.CASCADE)
   group_picture = models.ImageField(upload_to='group_pics/', null=True, blank=True)
   members = models.ManyToManyField(User, related_name='chat_groups')



class Message(models.Model):
   owner = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
   timestamp = models.DateTimeField(auto_now_add=True)
   message = models.TextField(max_length=250, null=False, blank=False)
   chat_owner = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')

   def save(self, *args, **kwargs) -> None:
      context_aux = self.message.strip()

      if not context_aux:
         raise ValidationError('Message content can not be empty')

      self.message = context_aux
      return super().save(*args, **kwargs)



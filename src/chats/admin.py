from django.contrib import admin
from .models import Contact, Message, ChatRoom

# Register your models here.
admin.site.register(Contact)
admin.site.register(Message)
admin.site.register(ChatRoom)
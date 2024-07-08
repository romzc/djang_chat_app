from django.shortcuts import render
from rest_framework import permissions, viewsets
from django.contrib.auth.models import User, Group
from .models import Profile
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .api.serializers import (
   UserSerializer, 
   GroupSerializer, 
   ProfileSerializer, 
   UserTokenObtainPairSerializer
)


class UserObtainTokenPairView(TokenObtainPairView):
   """
   """
   serializer_class = UserTokenObtainPairSerializer

   def get_serializer_context(self):
      context = super().get_serializer_context()
      context['request'] = self.request
      return context


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
   """
   API endpoint that allows users to be viewed and edited
   """
   queryset =  User.objects.all().order_by('-date_joined')
   serializer_class = UserSerializer
   authentication_classes = [JWTAuthentication]
   permission_classes = [permissions.IsAuthenticated]



class GroupViewSet(viewsets.ModelViewSet):
   """
   API endpoint that allows groups to be viewed and edited
   """
   queryset = Group.objects.all().order_by('name')
   serializer_class = GroupSerializer
   authentication_classes = [JWTAuthentication]
   permission_classes = [permissions.IsAuthenticated]


class ProfileViewSet(viewsets.ModelViewSet):
   """
   API endpoint that allows user profile to be viewed and edited
   """
   queryset = Profile.objects.all().order_by('-last_seen')
   serializer_class = ProfileSerializer
   authentication_classes = [JWTAuthentication]
   permission_classes = [permissions.IsAuthenticated]
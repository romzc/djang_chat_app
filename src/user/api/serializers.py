import json
from django.contrib.auth.models import Group, User
from rest_framework import serializers
from ..models import Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
   """
   Token serializer, with @classmethod removed because it needs an instance 
   to  get context.
   """
   def get_token(cls, user):
      token = super().get_token(user)
      context = cls.context
      user_data = UserSerializer(user, context=context).data
      token['user'] = user_data
      return token


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
   """
   Profile serializer
   """
   username = serializers.SerializerMethodField()
   email = serializers.SerializerMethodField()

   class Meta:
      model = Profile
      fields = ['id', 'name', 'surname', 'last_seen', 'username', 'email', 'avatar']

   def get_username(self, obj):
      return obj.user.username

   def get_email(self, obj):
      return obj.user.email


class UserSerializer(serializers.ModelSerializer):
   """
   User serializer
   """
   name = serializers.SerializerMethodField()
   surname = serializers.SerializerMethodField()
   last_seen = serializers.SerializerMethodField()
   avatar = serializers.SerializerMethodField()

   class Meta:
      model = User
      fields = ['id', 'username', 'email', 'name', 'surname', 'last_seen', 'avatar'] # 

   def get_name(self, obj):
      try:
         profile = obj.profile
         return profile.name
      except Profile.DoesNotExist:
         return None

   def get_surname(self, obj):
      try:
         profile = obj.profile
         return profile.surname
      except Profile.DoesNotExist:
         return None

   def get_last_seen(self, obj):
      try:
         profile = obj.profile
         return profile.last_seen.isoformat()
      except Profile.DoesNotExist:
         return None

   def get_avatar(self, obj):
      try:
         profile = obj.profile
         if profile.avatar:
            request = self.context.get('request', None)
            if request:
               return request.build_absolute_uri(profile.avatar.url)
            return profile.avatar.url
         return None
      except Profile.DoesNotExist:
         return None

   def create(self, validated_data):
      return super().create(validated_data)
  

class GroupSerializer(serializers.HyperlinkedModelSerializer):
   """
   Group serializer
   """
   class Meta:
      model = Group
      fields = ['id', "url", "name"]
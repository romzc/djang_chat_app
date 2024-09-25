from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import mixins, generics, serializers, permissions, response, status
from .models import Contact
from .services import create_contact

class ContactListView(mixins.ListModelMixin, generics.GenericAPIView):

   class UserSerializer(serializers.ModelSerializer):
      class Meta:
        model = User
        fields = ['id', 'username', 'email']

   class ContactSerializer(serializers.ModelSerializer):
      user = serializers.SerializerMethodField()
      contact = serializers.SerializerMethodField()

      class Meta:
         model = Contact
         fields = ('id', 'user', 'contact')
   
      def get_user(self, obj):        
         return ContactListView.UserSerializer(obj.user).data
         
      def get_contact(self, obj):
         return ContactListView.UserSerializer(obj.contact).data

   queryset = Contact.objects.all()
   serializer_class = ContactSerializer
   authentication_classes = [JWTAuthentication]
   permission_classes = [permissions.IsAuthenticated]

   def get_queryset(self):
      user = self.request.user
      return Contact.objects.filter(user=user)

   def get(self, request, *args, **kwargs):
      return self.list(request, *args, **kwargs)


class ContactCreateView(mixins.CreateModelMixin, generics.GenericAPIView):

   class UserSerializer(serializers.ModelSerializer):
      class Meta:
        model = User
        fields = ['id', 'username', 'email']

   class InputSerializer(serializers.ModelSerializer):
      class Meta:
         model = Contact
         fields = ('contact',)
   
   class OutputSerializer(serializers.Serializer):
      id = serializers.IntegerField()
      user = serializers.SerializerMethodField()
      contact = serializers.SerializerMethodField()

      def get_user(self, obj):        
         return ContactCreateView.UserSerializer(obj.user).data
         
      def get_contact(self, obj):
         return ContactCreateView.UserSerializer(obj.contact).data
   
   queryset = Contact.objects.all()
   serializer_class = InputSerializer
   authentication_classes = [JWTAuthentication]
   permission_classes = [permissions.IsAuthenticated]
      
   def post(self, request, *args, **kwargs):
      user = request.user
      serializer = self.InputSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      new_contact = create_contact(user=user, **serializer.validated_data)
      
      return response.Response(status=status.HTTP_201_CREATED, 
                               data=self.OutputSerializer(new_contact).data
                              )

# class ChatRoomListView(mixins.ListModelMixin, generics.GenericAPIView):
#    class 
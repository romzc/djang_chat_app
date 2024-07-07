from django.db import models
from django.contrib.auth.models import User

"""
Notes:
related_names, is useful to define inverse field name to the related model
for example:
We can access profile from User model, just using User.profile.all(), otherwise it's necessary 
to User.profile_set.all()

Its a nicely way to solve it.
"""

# Create your models here.
class Profile(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
   name = models.CharField(max_length=20, null=False, blank=False)
   surname = models.CharField(max_length=20, null=False, blank=False)
   last_seen = models.DateTimeField(auto_now=True)
   avatar = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

   def __str__(self) -> str:
      return f"{self.name} {self.surname}"



import jwt
from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from urllib.parse import parse_qs
from channels.auth import AuthMiddlewareStack


@database_sync_to_async
def get_user(token):
   try:
      payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
      user = User.objects.get(id=payload['user_id'])
      return user
   except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
      return AnonymousUser
   

class JWTAuthMiddleware(BaseMiddleware):
   
   async def __call__(self, scope, receive, send):
      query_string = parse_qs(scope['query_string'].decode())
      token = query_string.get('token', [None])[0]
      scope['user'] = await get_user(token)
      return await super().__call__(scope, receive, send)
   
   
def JWTAuthMiddlewareStack(inner):
   return JWTAuthMiddleware(inner)

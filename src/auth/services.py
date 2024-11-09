from database import async_session_maker
from src.users.services import UsersSercvices
class AuthServices:
   async def auth(data):
      async with async_session_maker() as session:
          user= UsersSercvices.get_user_by_email(email=data.email)
         #  ДОПИСАТЬ 
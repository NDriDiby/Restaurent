from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User


class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email = username)
            success = user.check_password(password)
            if success:
                return user
        except User.DoesNotExist:
            pass
        return None
    
    def get_user(self,id):
        try:
            return User.objects.get(pk=id)
        except:
            return None

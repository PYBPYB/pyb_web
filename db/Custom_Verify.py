from apps.user.models import User
from django.contrib.auth.backends import ModelBackend


# 自定义实现邮箱验证，而不是默认的偏要username验证
class EmailBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user

        except Exception as e:
            return None


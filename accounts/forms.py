from .models import User
from django.contrib.auth.forms import UserCreationForm # 장고가 미리 만들어놓은 form임

class CustomUserCreationForm(UserCreationForm):
    class Meta():
        model = User
        fields = ('username',)
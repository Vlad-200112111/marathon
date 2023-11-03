from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import *


class UserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("email",)


class UserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("email",)
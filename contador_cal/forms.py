from django import forms
from .models import Alimento, Comida, Ingrediente, Usuario
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

class alimento_form_model(forms.ModelForm):

    class Meta:
        model=Alimento
        fields='__all__'

class Perfil_Usuario(UserCreationForm):
    class Meta:
        model=get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')

class Ficha_Usuario(forms.ModelForm):

    class Meta:
        model=Usuario
        fields='altura', 'edad', 'peso', 'genero', 'objetivo', 'actividad'




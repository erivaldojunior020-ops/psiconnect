from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class AlunoRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'aluno'
        if commit:
            user.save()
        return user

class ProfessorLoginForm(AuthenticationForm):
    pass  # usa autenticação normal

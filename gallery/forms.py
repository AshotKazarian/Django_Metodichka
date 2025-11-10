from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile, Work
import re

class UserRegisterForm(forms.ModelForm):
    """Минимальная форма регистрации"""
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=1
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Имя'
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Фамилия'
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': 'Никнейм',
        }
        help_texts = {
            'username': 'Только латинские буквы, цифры и символы @/./+/-/_',
        }
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z0-9@.+_-]+$', username):
            raise forms.ValidationError(
                'Никнейм может содержать только латинские буквы, цифры и символы @/./+/-/_'
            )
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Этот никнейм уже занят')
        return username
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserLoginForm(AuthenticationForm):
    """Форма входа пользователя"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'
        self.fields['username'].label = 'Никнейм'

class ProfileUpdateForm(forms.ModelForm):
    """Форма обновления профиля"""
    first_name = forms.CharField(
        max_length=30, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Имя'
    )
    last_name = forms.CharField(
        max_length=30, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Фамилия'
    )
    
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.user.first_name = self.cleaned_data['first_name']
            profile.user.last_name = self.cleaned_data['last_name']
            profile.user.save()
            profile.save()
        return profile

class WorkCreateForm(forms.ModelForm):
    """Форма создания работы для обычных пользователей"""
    class Meta:
        model = Work
        fields = ['title', 'description', 'year', 'genre', 'tools', 'proportion', 'tags', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'year': forms.NumberInput(attrs={'min': 1900, 'max': 2025}),
            'tools': forms.CheckboxSelectMultiple(),
            'genre': forms.Select(attrs={'class': 'form-control'}),
            'proportion': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name in self.fields:
            if field_name not in ['tools'] and 'class' not in self.fields[field_name].widget.attrs:
                self.fields[field_name].widget.attrs['class'] = 'form-control'
        
        self.fields['genre'].required = False
        self.fields['proportion'].required = False
        self.fields['tools'].required = False
        self.fields['tags'].required = False
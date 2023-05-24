from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class LoginForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

class SignupForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    nickname = forms.CharField(max_length=255, label='Никнейм')
    avatar = forms.ImageField(label='Загрузить аватар', required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'nickname', 'avatar')


class ProfileForm(forms.ModelForm):
    username = forms.CharField(label='Логин', max_length=150)
    email = forms.EmailField(label='Email')
    nickname = forms.CharField(label='Никнейм', max_length=255)
    avatar = forms.ImageField(label='Загрузите аватарку', required=False)

    class Meta:
        model = Profile
        fields = ['username', 'email', 'nickname', 'avatar']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].initial = self.instance.user.username
        self.fields['email'].initial = self.instance.user.email
        self.fields['nickname'].initial = self.instance.nickname

    def save(self, commit=True):
        profile = super(ProfileForm, self).save(commit=False)
        profile.user.username = self.cleaned_data['username']
        profile.user.email = self.cleaned_data['email']
        profile.user.save()
        profile.nickname = self.cleaned_data['nickname']
        if commit:
            profile.save()
        return profile

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']

class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, label='Текст ответа')

from socket import fromshare
from django.forms import ModelForm 

from tkinter import Widget 


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms 
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

from .models import Thought, Profile

# create a new user
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

#  login a user form
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


#  post a thought
class ThoughtPostForm(forms.ModelForm):
    class Meta:
        model = Thought

        fields = ['title','content']
        exclude = ['user']


#  update the thought
class ThoughtUpdateForm(forms.ModelForm):
    class Meta:
        model = Thought

        fields = ['title','content']
        exclude = ['user']


#  update user details
class UpdateUserForm(forms.ModelForm):
    password = None

    class Meta:
        model = User
        fields = ['username', 'email']
        exclude = ['password1','password2']


#  update profile
class UpdateProfileForm(forms.ModelForm):
    profile_pic = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control-file'}))
    about= forms.CharField(widget=TextInput())
    place=  forms.CharField(widget=TextInput())
    link = forms.CharField(widget=TextInput())

    class Meta:

        model = Profile
        fields = ['profile_pic','about','place','link']

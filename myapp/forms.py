#-*- coding: utf-8 -*-
from django import forms

class SearchForm(forms.Form):
   text = forms.CharField(max_length = 100)

class LoginForm(forms.Form):
   username = forms.CharField(max_length = 100)
   password = forms.CharField(max_length = 100)

class RegisterForm(forms.Form):
   username = forms.CharField(max_length = 100)
   password = forms.CharField(max_length = 100)

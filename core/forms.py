from django import forms
from django.forms import ModelForm, Form
from core import models
from django.contrib.auth.models import User


class LoginForm(Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=18, widget=forms.PasswordInput())

class SignUpForm(forms.ModelForm):
    categories = models.Category.objects.all()
    category = forms.ModelChoiceField(queryset=categories, widget=forms.Select(attrs={"class":"custom-select-box", "id":"ui-id-1", "style":"display: none;"}))
    username = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=100)
    last_name =  forms.CharField(max_length=100)
    password = forms.CharField(max_length=18, widget=forms.PasswordInput())
    email = forms.EmailField()
    confirm_password = forms.CharField(max_length=18, widget=forms.PasswordInput())
    class Meta:
        model = models.UserExtended
        fields = "__all__"
        exclude = ("is_admin",)
        widgets = {
            "is_instructor": forms.CheckboxInput(attrs={"hidden":""}),
            "is_student": forms.CheckboxInput(attrs={"hidden":""}),
            
        }
    
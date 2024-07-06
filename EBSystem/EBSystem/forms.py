from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

class LoginForm(forms.Form):
    USER_TYPE = [
        ('Select', 'Select'),
        ('Admin', 'Admin'),
        ('Employee', 'Employee'),
        ('Customer', 'Customer'),
      
    ]
     
    userType = forms.ChoiceField(choices=USER_TYPE, widget=forms.Select(attrs={'placeholder': 'Select User Type'}),required=True, label="User Type")
    userName = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter User Name'}),required=True, label="User Name")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),required=True,label="Password")
    
class SignUpForm(forms.Form):
    
    f_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter First Name'}),required=True, label='First Name')
    l_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Last Name'}),required=True, label='Last Name')
    phone_no = forms.IntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)], widget=forms.NumberInput(attrs={'placeholder': 'Enter Mobile Number'}),required=True, label='Phone Number')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Enter your Email ID'}), label="Email Id")
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter User Name'}),required=True, label="User Name")
  
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),required=True, label="Password")    
    repassword = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your password again'}),required=True,label="Re-Password")
     
    
    
  
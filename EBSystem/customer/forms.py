from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
 
class SendWAMessageForm(forms.Form):
    MONTH_CHOICES = [
        ('Select', 'Select'),
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December'),
    ]
    phone = forms.IntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)], widget=forms.NumberInput(attrs={'placeholder': 'Enter Whatsapp Mobile Number'}),required=True)
    reminderSelectMonth = forms.ChoiceField(choices=MONTH_CHOICES, widget=forms.Select(attrs={'placeholder': 'Select Reminder Month'}),required=True)
    billAmount = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'Enter Bill Amount in Rs.'}),required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Enter Reminder Message . . .'}),max_length=200,required=True)
    
class SendEmailForm(forms.Form):
    MONTH_CHOICES = [
        ('Select', 'Select'),
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December'),
    ]
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':"Enter Receiver Email Address"}),required=True)
    reminderSelectMonth = forms.ChoiceField(choices=MONTH_CHOICES, widget=forms.Select(attrs={'placeholder': 'Select Reminder Month'}),required=True)
    billAmount = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'Enter Bill Amount in Rs.'}),required=True)
    subject = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter Email Subject'}),required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Enter Reminder Message . . .'}),max_length=200,required=True)   
    
class CalculateBillForm(forms.Form):
    MONTH_CHOICES = [
        ('Select', 'Select'),
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December'),
    ]
    meterno = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Please Enter Customer Meter no'}), max_length=10, required=True)
    generateBillMonth = forms.ChoiceField(choices=MONTH_CHOICES, widget=forms.Select(attrs={'placeholder': 'Select Month'}),required=True)
    unit = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'Enter Unit.'}),required=True)
 


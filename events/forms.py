from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Event, CSVFile

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'date', 'venue', 'highlights', 'form_link', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'venue': forms.TextInput(attrs={'class': 'form-control'}),
            'highlights': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'form_link': forms.URLInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

class CSVUploadForm(forms.ModelForm):
    class Meta:
        model = CSVFile
        fields = ['file', 'description']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief description of this data'}),
        }

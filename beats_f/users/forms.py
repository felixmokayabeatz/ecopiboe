# forms.py

from django import forms
from .models import UserResponse

class EcoFootprintForm(forms.ModelForm):
    class Meta:
        model = UserResponse
        fields = ['response']
        widgets = {
            'response': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        }


class BookRecommendationForm(forms.Form):
    title = forms.CharField(label='Title', required=False)
    author = forms.CharField(label='Author', required=False)
    publishDate = forms.IntegerField(label='Publication Year', required=False)
    description = forms.CharField(label='Description', required=False)
    cover_photo = forms.ImageField(label='Cover Photo', required=False)
    
    
from .models import UploadFile

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadFile
        fields = ['file', 'file_type']
        
        
        
        
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
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
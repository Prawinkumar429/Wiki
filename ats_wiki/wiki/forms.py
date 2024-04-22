from django import forms
from .models import FileUpload,Wiki



class SearchForm(forms.Form):
    query = forms.CharField(label='Search')
    
class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ['file']
        widgets = {'file': forms.ClearableFileInput(attrs={'allow_multiple_selected': True, 'required': False})}
        
class WikiEntryForms(forms.ModelForm):
    class Meta:
        model = Wiki
        fields = ['subject', 'description']  # Include the fields you want to display/edit
        widgets = {
            'subject': forms.TextInput(),
            'description': forms.Textarea(),
        }

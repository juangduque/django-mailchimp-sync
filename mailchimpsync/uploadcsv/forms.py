from django import forms
from .models import UploadNewFile

class UploadNewFileForm(forms.ModelForm):
    class Meta:
        model = UploadNewFile
        fields = ['csv_file']
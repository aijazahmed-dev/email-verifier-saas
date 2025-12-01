from django import forms

class UploadCSVForm(forms.Form):
    file = forms.FileField(label="Upload CSV file with emails")

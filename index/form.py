from django import forms

class PropertyImageForm(forms.Form):
    file = forms.ImageField()

class PropertyImportantForm(forms.Form):
    name = forms.CharField(max_length=50)
    number = forms.CharField(max_length=50)
    serial = forms.CharField(max_length=50)

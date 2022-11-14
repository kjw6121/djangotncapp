from django import forms

class Register(forms.Form):
    your_name = forms.CharField(label='성명', max_length=7),
    pw = forms.CharField(label='패스워드', max_length=10),
    
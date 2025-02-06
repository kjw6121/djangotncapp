from django.contrib import admin
from .models import ScanData

# Register your models here.
@admin.register(ScanData)
class ScanDataAdmin(admin.ModelAdmin):
   def clean_password2(self):
       pass1 = self.cleaned_data['password1']
       pass2 = self.cleaned_data['password2']
       if pass1 and pass2 and pass1 != pass2:
           raise forms.ValidationError('password didn"t match')
       return pass2

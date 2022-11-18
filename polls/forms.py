from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import Boxtr


class CreateUserForm(UserCreationForm): # 내장 회원가입 폼을 상속받아서 확장한다.
    
    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def save(self, commit=True): # 저장하는 부분 오버라이딩
        user = super(CreateUserForm, self).save(commit=False) # 본인의 부모를 호출해서 저장하겠다.
        if commit:
            user.save()
        return user


class boxform(forms.ModelForm):
    class Meta:
        model = Boxtr
        fields = ("arrival", "wet", "box1", "box1_qty", "box2", "box2_qty", 
                  "box3", "box3_qty", "box4", "box4_qty", "box5", "box5_qty")
        labels = {
            
            "arrival": "도착예정시간",
            "wet" : "침수여부",
            "box1": "박스",
            "box1_qty": "수량",
            "box2": "박스",
            "box2_qty": "수량",
            "box3": "박스",
            "box3_qty": "수량",
            "box4": "박스",
            "box4_qty": "수량",
            "box5": "박스",
            "box5_qty": "수량",
        }
        
        widgets = {
            'arrival': forms.Select(attrs={'class':'form_control'}),
            'wet' : forms.Select(attrs={'class':'form_control'}),
            'box1' : forms.Select(attrs={'class':'form_control'}),
            'box1_qty' : forms.Select(attrs={'class':'form_control'}),
            'box2' : forms.Select(attrs={'class':'form_control'}),
            'box2_qty' : forms.Select(attrs={'class':'form_control'}),
            'box3' : forms.Select(attrs={'class':'form_control'}),
            'box3_qty' : forms.Select(attrs={'class':'form_control'}),
            'box4' : forms.Select(attrs={'class':'form_control'}),
            'box4_qty' : forms.Select(attrs={'class':'form_control'}),
            'box5' : forms.Select(attrs={'class':'form_control'}),
            'box5_qty' : forms.Select(attrs={'class':'form_control'}),
            
            
                                  
            }
        
        def save(self, commit=True):
                post = Boxtr(self.cleaned_data)
                if commit:
                    post.save()
                return post
from django import forms
from django.contrib.auth.models import User
from . import models

class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=150)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))




class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']



class StudentUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']

class StudentExtraForm(forms.ModelForm):
    class Meta:
        model=models.StudentExtra
        fields=['Kelas',]

class BookForm(forms.ModelForm):
    class Meta:
        model = models.Book
        fields = ['name', 'isbn', 'copies', 'author', 'category']

class IssuedBookForm(forms.Form):
    isbn2 = forms.CharField(max_length=13, label='ISBN')
    kelas2 = forms.ChoiceField(choices=[], label='Kelas')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        kelas_choices = [(kelas, kelas) for kelas in models.StudentExtra.objects.values_list('Kelas', flat=True).distinct()]
        self.fields['kelas2'].choices = [('', 'Select Kelas')] + kelas_choices



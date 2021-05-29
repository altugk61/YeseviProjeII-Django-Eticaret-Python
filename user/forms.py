from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, Select, FileInput

from home.models import UserProfile


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': TextInput(attrs={'class': 'input',
                                         'placeholder': 'username',
                                         'style':'background:#F0F0E9; border: 0 none;margin-bottom:10px;padding: 10px; width:100%; font-weight: 300'}),
            'email': EmailInput(attrs={'class': 'input',
                                       'placeholder': 'email',
                                       'style':'background:#F0F0E9; border: 0 none;margin-bottom:10px;padding: 10px; width:100%; font-weight: 300'}),
            'first_name': TextInput(attrs={'class': 'input',
                                           'placeholder': 'first_name',
                                           'style':'background:#F0F0E9; border: 0 none;margin-bottom:10px;padding: 10px; width:100%; font-weight: 300'}),
            'last_name': TextInput(attrs={'class': 'input',
                                          'placeholder': 'last_name',
                                          'style':'background:#F0F0E9; border: 0 none;margin-bottom:10px;padding: 10px; width:100%; font-weight: 300'}),
        }


CITY = [
    ('Istanbul', 'Istanbul'),
    ('Ankara', 'Ankara'),
    ('Izmir', 'Izmir'),
]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'city', 'country', 'image')
        widgets = {
            'phone': TextInput(attrs={'class': 'input', 'placeholder': 'phone', 'style':'background:#F0F0E9; border: 0 none;margin-bottom:10px;padding: 10px; width:100%; font-weight: 300'}),
            'address': TextInput(attrs={'class': 'input', 'placeholder': 'address', 'style':'background:#F0F0E9; border: 0 none;margin-bottom:10px;padding: 10px; width:100%; font-weight: 300'}),
            'city': Select(attrs={'class': 'input', 'placeholder': 'city'}, choices=CITY),
            'country': TextInput(attrs={'class': 'input', 'placeholder': 'country', 'style':'background:#F0F0E9; border: 0 none;margin-bottom:10px;padding: 10px; width:100%; font-weight: 300'}),
            'image': FileInput(attrs={'class': 'input', 'placeholder': 'image', }),
        }

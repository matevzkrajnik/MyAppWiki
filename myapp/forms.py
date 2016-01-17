from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from bootstrap3_datetime.widgets import DateTimePicker
from .models import User, Stran, UporabnikProfil


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ime', 'required': 'true'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Priimek', 'required': 'true'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-Mail', 'required': 'true', }),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Uporabniško ime', 'required': 'true'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Geslo', 'required': 'true'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Potrditev gesla', 'required': 'true'})

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()
        return user


class DodajStranForm(forms.ModelForm):

    class Meta:
        model = Stran
        fields = ('naslov', 'vsebina', 'sporocilo')
        exclude = ['avtor', 'datum_nastanka']
        widgets = {
            'naslov': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Naslov', 'required': 'true'}),
            'vsebina': forms.Textarea(attrs={'class': 'form-control', 'style': 'resize:none', 'placeholder': 'Vsebina strani', 'required': 'true'}),
            'sporocilo': forms.Textarea(attrs={'class': 'form-control', 'style': 'resize:none', 'placeholder': 'Na kratko napišite vsebino strani', 'required': 'true', }),
        }


class SlikaUploadForm(forms.ModelForm):

    class Meta:
        model = UporabnikProfil
        fields = ('slika_profila',)
        exclude = ['uporabnik']


class UporabnikUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ime', 'required': 'true'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Priimek', 'required': 'true'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail', 'required': 'true'}),
        }
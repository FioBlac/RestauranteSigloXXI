from django import  forms
from django.contrib.auth.models import  User

class Registro(forms.Form):
    username = forms.CharField(required=True, min_length=5, max_length=40,
    widget = forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Nombre de Usuario'
    }))
    correo=forms.EmailField(required=True,widget=forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder':'ejemplo@gmail.com'
    }))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Contraseña'
    }))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Confirmar contraseña'
    }))




    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Usuario ya creado')
        return username 

    def clean_email(self):
        correo=self.cleaned_data.get('email') 

        if User.objects.filter(email=correo).exists():
            raise forms.ValidationError('Correo ya registrado') 

        return correo 

    def clean(self):
        cleaned_data = super().clean()

        if self.cleaned_data.get('password2') !=  cleaned_data.get('password'):
                self.add_error('password2','La contraseña no coincide')

    def save(self):
        return User.objects.create_user(
            self.cleaned_data.get('username'),
            self.cleaned_data.get('email'),
            self.cleaned_data.get('password'),
            

        )
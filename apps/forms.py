from django import forms
from django.db.models import fields
from .models import Mesa, Reserva
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import  User

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['id_reserva','cantidad_personas','fecha_reserva','comentario','fecha_vence']

class DatosReservaForm(forms.Form):
    cantidad_personas = forms.CharField()
    fecha = forms.DateTimeField()
    hora = forms.CharField()
    comentario = forms.CharField()

class MesaForm(forms.ModelForm):
    class Meta:
        model = Mesa
        fields = ['id_mesa', 'numero_mesa','disponibilidad']

class datosAgregarMesaForm(forms.Form):
    numMesaAgg = forms.CharField()
    dispMesaAgg = forms.CharField()

class CustomUserCreationFrom (UserCreationForm):
    
    class Meta:
        model = User
        fields = ["username","first_name","last_name","email","password1","password2"]

class CustomUserCreationFrom2 (UserCreationForm):
    
    class Meta:
        model = User
        fields = ["username","first_name","last_name","email","password1","password2"]


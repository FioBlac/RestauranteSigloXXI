from django import forms
from .models import Reserva

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['id_reserva','cantidad_personas','fecha_reserva','comentario','fecha_vence']

class DatosReservaForm(forms.Form):
    cantidad_personas = forms.CharField()
    fecha = forms.DateTimeField()
    hora = forms.CharField()
    comentario = forms.CharField()
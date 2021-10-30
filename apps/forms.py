from django import forms
from django.db.models import fields
from .models import Mesa, Reserva

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
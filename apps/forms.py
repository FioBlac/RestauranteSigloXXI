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

class AgregarProductoForm(forms.Form):
    id_bodega = forms.CharField()
    nombre_alimento = forms.CharField()
    t_conservacion = forms.CharField()
    cantidad_alimento = forms.CharField()
    fecha_caducidad = forms.DateTimeField()
    zona_refrigeracion = forms.CharField()
    tipo_alimento = forms.CharField()

class EliminarProductoForm(forms.Form):
    id_producto_borrar = forms.CharField()


class EliminarUsuarioForm(forms.Form):
    id_usuario_borrar = forms.CharField()

class EliminarMesaForm(forms.Form):
    id_mesa_borrar = forms.CharField()


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

    """def clean_password2(self, *args, **kwargs):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return password2"""

class CustomUserCreationFrom2 (UserCreationForm):
    
    class Meta:
        model = User
        fields = ["username","first_name","last_name","email","password1","password2"]


    """def clean_password2(self, *args, **kwargs):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return password2"""


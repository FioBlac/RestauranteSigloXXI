from django import forms
from django.db.models import fields
from .models import Mesa, Reserva
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import  User
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.utils.translation import gettext, gettext_lazy as _


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

class cambiarEstadoPedidoForm(forms.Form):
    cambiarEstado = forms.CharField()



class CustomUserCreationFrom(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': 'Las contraseñas no coinciden.',
    }
    password1 = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Confirmación de contraseña",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ("username","first_name","last_name","email")
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserCreationFrom2(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': 'Las contraseñas no coinciden.',
    }
    password1 = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Confirmación de contraseña",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ("username","first_name","last_name","email")
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

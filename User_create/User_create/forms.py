from django import forms
from DB.models import *

##################################################################


class UserCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control text-center'

    class Meta:
        model = Users
        fields = (
            "username",
            "first_name",
            "last_name",
            "password",
            "email",
        )

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "placeholder": "Username",
                    "autofocus": "True",
                    "type": "text",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "placeholder": "Nombre",
                    "type": "text",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "placeholder": "Apellido",
                    "type": "text",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "mail@example.com",
                }
            ),
            "password": forms.PasswordInput(
                attrs={
                    "placeholder": "Password",
                }
            ),
        }

        exclude = [
            "address",
            "number_address",
            "city",
            "country",
            "phone_number",
            "dni",
            "image_user",
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)
        return instance


class UserEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserEditForm,self).__init__(*args, **kwargs)
        self.fields["country"].choices = [
            ("", "-Country-")]+list(self.fields["country"].choices)[1:]
        self.fields['username'].label = "Nombre de usuario"
        self.fields['first_name'].label = "Nombre"
        self.fields['last_name'].label = "Apellido"
        self.fields['dni'].label = "DNI"
        self.fields['address'].label = "Direccion"
        self.fields['number_address'].label = "Numero de puerta"
        self.fields['phone_number'].label = "Telefono"
        self.fields['image_user'].label = "Imagen"
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control text-center'

    class Meta:
        model = Users
        fields = (
            "username",
            "first_name",
            "last_name",
            "dni",
            "country",
            "address",
            "number_address",
            "phone_number",
            "image_user",
        )

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "placeholder": "Username",
                    "autofocus": "True",
                    "type": "text",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "placeholder": "Nombre",
                    "type": "text",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "placeholder": "Apellido",
                    "type": "text",
                }
            ),
            "dni": forms.NumberInput(
                attrs={
                    "placeholder": "DNI",
                    "type": "number",
                    "min_length": 8,
                    "max_length": 8,
                }
            ),
            "country": forms.Select(
                attrs={
                    "placeholder": "Pais",
                    "type": "text",
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "placeholder": "Direccion",
                    "type": "text",
                }
            ),
            "number_address": forms.NumberInput(
                attrs={
                    "placeholder": "Numero de puerta",
                    "type": "number",
                }
            ),
            "phone_number": forms.NumberInput(
                attrs={
                    "placeholder": "Telefono",
                    "type": "number",
                }
            ),
            "image_user": forms.FileInput(
                attrs={
                    "placeholder": "Imagen",
                    "type": "file",
                }
            ),
        }

        exclude = [
            "password",
            "email",
        ]

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data["error"] = form.errors
        except Exception as e:
            data["error"] = str(e)
        return data


class ClientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.fields["gender"].choices = [("", "Gender")]+list(self.fields["gender"].choices)[1:]

        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control text-center'

    class Meta:
        model = Client
        fields = (
            "name",
            "dni",
            "gender",
        )

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Name",
                    "autofocus": "True",
                    "type": "text",
                }
            ),
            "dni": forms.NumberInput(
                attrs={
                    "placeholder": "DNI",
                    "type": "number",
                }
            ),
            "gender": forms.Select(
                attrs={
                    "placeholder": "Apellido",
                    "type": "text",
                }
            ),

        }

        exclude = [
            "user_create",
            "user_update",
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)
        return instance

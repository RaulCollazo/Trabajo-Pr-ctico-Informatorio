from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        # solo los campos que querés completar
        fields = ("username", "email", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Agregar clases Bootstrap y placeholders
        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})

        self.fields["username"].widget.attrs.update({"placeholder": "Elegí como te verán los demás"})
        self.fields["email"].widget.attrs.update({"placeholder": "tu@correo.com"})
        self.fields["first_name"].widget.attrs.update({"placeholder": "Nombre"})
        self.fields["last_name"].widget.attrs.update({"placeholder": "Apellido"})
        self.fields["password1"].widget.attrs.update({"placeholder": "Contraseña"})
        self.fields["password2"].widget.attrs.update({"placeholder": "Repetir contraseña"})


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Usuario"})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Contraseña"})
    )


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "edad", "avatar")
        widgets = {"avatar": forms.ClearableFileInput(attrs={"class": "form-control"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != "avatar":
                field.widget.attrs.update({"class": "form-control"})
        self.fields["first_name"].widget.attrs["placeholder"] = "Nombre"
        self.fields["last_name"].widget.attrs["placeholder"] = "Apellido"
        self.fields["email"].widget.attrs["placeholder"] = "tu@correo.com"
        self.fields["edad"].widget.attrs["placeholder"] = "Edad"

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")
        if not avatar:
            return avatar
        if getattr(avatar, "size", 0) > 2 * 1024 * 1024:
            raise forms.ValidationError("La imagen no puede superar 2MB.")
        content_type = getattr(avatar, "content_type", "")
        if not content_type.startswith("image/"):
            raise forms.ValidationError("Archivo inválido: debe ser una imagen.")
        return avatar

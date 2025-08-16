from django import forms
from .models import Comentario

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ["contenido"]
        widgets = {
            "contenido": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Escribí tu comentario…"}),
        }
        labels = {"contenido": ""}

from django import forms
from .models import Post, Categoria, Tag

class PostForm(forms.ModelForm):
    categorias = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.none(),
        widget=forms.SelectMultiple(attrs={"class": "form-select", "size": 6}),
        required=False,
        label="Categorías"
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.none(),
        widget=forms.SelectMultiple(attrs={"class": "form-select", "size": 6}),
        required=False,
        label="Tags"
    )

    class Meta:
        model = Post
        fields = ["titulo", "resumen", "contenido", "categorias", "tags", "imagen"]  # <-- incluir imagen
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "resumen": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "contenido": forms.Textarea(attrs={"class": "form-control", "rows": 10}),
            "imagen": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["categorias"].queryset = Categoria.objects.all().order_by("nombre")
        self.fields["tags"].queryset = Tag.objects.all().order_by("nombre")

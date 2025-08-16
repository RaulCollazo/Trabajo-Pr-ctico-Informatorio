from django import forms
from .models import Post, Categoria, Tag

class PostForm(forms.ModelForm):
    categorias = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.none(),
        widget=forms.SelectMultiple(attrs={"class": "form-select", "size": 6}),
        required=False,
        label="Categorías"
    )
    nueva_categoria = forms.CharField(
        required=False,
        label="Nueva categoría",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Escribe una nueva categoría"
        })
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.none(),
        widget=forms.SelectMultiple(attrs={"class": "form-select", "size": 6}),
        required=False,
        label="Tags"
    )

    class Meta:
        model = Post
        fields = ["titulo", "resumen", "contenido", "categorias", "nueva_categoria", "tags", "imagen"]
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

    def save(self, commit=True):
        post = super().save(commit=False)
        if commit:
            post.save()

        # Guardar categorías seleccionadas
        if self.cleaned_data.get("categorias"):
            post.categorias.set(self.cleaned_data["categorias"])

        # Crear nueva categoría si el usuario la ingresó
        nueva_cat = self.cleaned_data.get("nueva_categoria")
        if nueva_cat:
            categoria, creada = Categoria.objects.get_or_create(nombre=nueva_cat.strip())
            post.categorias.add(categoria)

        return post

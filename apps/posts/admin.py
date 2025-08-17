from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Post, Categoria, Tag

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'autor', 'fecha_hora')
    list_filter = ('fecha_hora', 'autor', 'categorias', 'tags')
    search_fields = ('titulo', 'resumen', 'contenido', 'autor__username')
    date_hierarchy = 'fecha_hora'
    filter_horizontal = ('categorias', 'tags')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'parent')
    search_fields = ('nombre',)
    list_filter = ('parent',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)
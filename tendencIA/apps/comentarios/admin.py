from django.contrib import admin
from .models import Comentario

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'usuario', 'fecha_hora')
    search_fields = ('contenido', 'post__titulo', 'usuario__username')
    list_filter = ('fecha_hora', 'usuario')
    date_hierarchy = 'fecha_hora'
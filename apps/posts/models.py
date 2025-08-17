from django.db import models
from django.conf import settings  # para settings.AUTH_USER_MODEL

class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subcategorias'
    )

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'


class Tag(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']


class Post(models.Model):
    titulo = models.CharField(max_length=200)
    resumen = models.CharField(max_length=300)
    contenido = models.TextField()
    fecha_hora = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    categorias = models.ManyToManyField(Categoria, related_name='posts', blank=True)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    
    imagen = models.ImageField(upload_to='post_images/', blank=True, null=True)

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['-fecha_hora']

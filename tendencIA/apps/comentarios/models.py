from django.db import models
from django.conf import settings

class Comentario(models.Model):
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comentarios'
    )
    contenido = models.TextField()
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentario de {self.usuario} en "{self.post.titulo}"'

    class Meta:
        ordering = ['-fecha_hora']

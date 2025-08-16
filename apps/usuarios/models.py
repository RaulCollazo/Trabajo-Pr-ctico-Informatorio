from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """
    Usuario del sistema con roles de acceso.
    Roles:
      - visitante: solo navega/filtra (no comenta)
      - lector: usuario registrado (puede comentar)
      - escritor: colaborador (gestiona posts y comentarios de otros)
      - admin: rol interno; además puede existir superuser de Django
    """
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    edad = models.PositiveIntegerField(blank=True, null=True)

    class Rol(models.TextChoices):
        VISITANTE = 'visitante', 'Visitante'
        LECTOR    = 'lector',    'Lector'
        ESCRITOR  = 'escritor',  'Escritor'
        ADMIN     = 'admin',     'Administrador'

    # 🔁 Cambio principal: por defecto ahora es LECTOR (miembro que puede comentar)
    rol = models.CharField(
        max_length=20,
        choices=Rol.choices,
        default=Rol.LECTOR,
    )

    # -------- Helpers útiles en vistas/plantillas --------
    @property
    def is_visitante(self) -> bool:
        return self.rol == self.Rol.VISITANTE

    @property
    def is_lector(self) -> bool:
        return self.rol == self.Rol.LECTOR

    @property
    def is_escritor(self) -> bool:
        return self.rol == self.Rol.ESCRITOR

    @property
    def is_admin_rol(self) -> bool:
        # Nota: esto es el rol de tu modelo, no confundir con is_superuser de Django
        return self.rol == self.Rol.ADMIN

    def puede_comentar(self) -> bool:
        # Visitante no; lector/escritor/admin sí
        return self.rol in (self.Rol.LECTOR, self.Rol.ESCRITOR, self.Rol.ADMIN)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['username']
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    # Opcional: agrega campos personalizados si tienes 'edad' y 'rol'
    fieldsets = UserAdmin.fieldsets + (
        ('Datos adicionales', {'fields': ('edad', 'rol')}),
    )
    list_display = UserAdmin.list_display + ('edad', 'rol')
    list_filter = UserAdmin.list_filter + ('rol',)
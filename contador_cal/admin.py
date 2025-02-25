from django.contrib import admin
from .models import Alimento, Ingrediente, Comida, Usuario, Diario, Pesos
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    model = Usuario
    fieldsets = UserAdmin.fieldsets + (
         (None, {'fields': ('altura', 'edad', 'peso','genero', 'objetivo', 'actividad')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
         (None, {'fields': ('altura', 'edad', 'peso', 'genero', 'objetivo', 'actividad')}),
    )
# Register your models here.
admin.site.register(Alimento),
admin.site.register(Ingrediente),
admin.site.register(Comida),
admin.site.register(Usuario, UsuarioAdmin),
admin.site.register(Diario),
admin.site.register(Pesos),

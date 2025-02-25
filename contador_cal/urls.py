from django.urls import path
from .views import *

urlpatterns = [
    #Inicio
    path('', Home.as_view(), name='home'),
    path('cerrar_sesion', Cerrar_sesion.as_view(), name='cerrar'),

    #Registrar
    path('registrarPerfil', RegistraPerfilUsuario.as_view(), name='registrar_perfil'),
    path('registrarDatos/<int:pk>', RegistraDatosUsuario.as_view(), name='registrar_Datos'),
    path('cancelarRegistro', cancelar_Registro, name='cancela_registro'),
    

    #Alimento
    path('crear_alimento', CrearAlimento.as_view(), name='crear_alimento'),
    path('listar_alimento', ListarAlimento.as_view(), name='listar_alimento'),
    path('editar_alimento/<int:pk>', EditarAlimento.as_view(), name='editar_alimento'),
    path('borrar_alimento/<int:pk>', BorrarAlimento.as_view(), name='borrar_alimento'),


    #Usuario
    path('editarFichaUsuario/<int:pk>', EditarFichaUsuario.as_view(), name='editar_ficha_usuario'),
    path('editarPerfilUsuario/<int:pk>', EditarPerfilUsuario.as_view(), name='editar_perfil_usuario'),

    #Funcionalidad
    path('añadir_alimento/<int:pk>', AñadirAlimento.as_view(), name='añadir_alimento'),
    path('pesos', Pesos_lista.as_view(), name='pesos'),
    path('guardar_peso', Guardar_peso.as_view(), name='guardar_peso'),


]
from django.shortcuts import render, get_object_or_404, redirect
from .forms import alimento_form_model, Perfil_Usuario, Ficha_Usuario
from .models import Alimento, Usuario, Diario, Pesos
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
import math
from django.core.paginator import Paginator
from datetime import date
from django.db import transaction
from django.contrib.auth import login
# Create your views here. Utilizar decored

class Inicio(TemplateView):
    template_name= 'contador_cal/index.html'

class Home(LoginRequiredMixin, TemplateView):
    template_name='contador_cal/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = Usuario.objects.get(id=self.request.user.id)
        context['usuario'] = usuario

        objetivo = usuario.objetivo
        altura = usuario.altura
        genero = usuario.genero
        edad = usuario.edad
        peso = usuario.peso
        actividad = usuario.actividad

        #Calorias a consumir
        if(objetivo and altura and genero and edad and peso and actividad):
            
            if(genero == "Masculino"):
                tmb = 5 + (10*peso)+(6.25*altura)-(5*edad)
            else:
                tmb =(10*peso)+(6.25*altura)-(5*edad) -161
            
            if(actividad == 'Nula'):
                calorias_mantenimiento = tmb*1.2
            elif(actividad == '1 a 2 veces en semana'):
                calorias_mantenimiento = tmb*1.375
            elif(actividad == '3 a 5 veces en semana'):
                calorias_mantenimiento = tmb*1.55
            elif(actividad == '6 a 7 veces en semana'):
                calorias_mantenimiento = tmb*1.725
            else:
                calorias_mantenimiento = tmb*1.9
            
            if(objetivo == 'Perder peso'):
                calorias = calorias_mantenimiento - 400
            elif(objetivo == 'Ganar peso'):
                calorias = calorias_mantenimiento + 400
            else:
                calorias = calorias_mantenimiento
            
            context['calorias_a_consumir'] = math.ceil(calorias)

            #calorias Consumidas
            diario_existente = Diario.objects.filter(usuario=usuario, fecha=date.today()).first()
        
            if diario_existente == None:
                calorias_consumidas=0
                context['calorias_consumidas']= calorias_consumidas

            else:
                calorias_consumidas= diario_existente.calorias
                context['calorias_consumidas']= calorias_consumidas

            #Calorias restantes
            context['calorias_restantes']=math.ceil(calorias) - calorias_consumidas

        return context

class Cerrar_sesion(TemplateView):
    template_name='registration/logout.html'

class CrearAlimento(LoginRequiredMixin, UserPassesTestMixin, CreateView): #Es necesrio estar logueado
    model=Alimento
    template_name='contador_cal/Alimento_Crear.html'
    form_class=alimento_form_model
    success_url=reverse_lazy('listar_alimento')

    def test_func(self):
        user = self.request.user
        return user.has_perm('app_name.add_alimento')
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para crear alimentos.')
        return redirect('listar_alimento')
    
    def form_valid(self, form):
        messages.success(self.request, 'Alimento creado correctamente')
        return super().form_valid(form)

class ListarAlimento(LoginRequiredMixin, ListView):
    model=Alimento
    template_name='contador_cal/Alimento_listado.html'
    context_object_name='alimentos'
    paginate_by = 5

    def get_queryset(self):
        query = super().get_queryset()
        filtro_nombre = self.request.GET.get('filtro_nombre')

        if filtro_nombre:
            query = query.filter(nombre__icontains = filtro_nombre)

        return query

class EditarAlimento(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model=Alimento
    template_name='contador_cal/Alimento_Editar.html'
    form_class=alimento_form_model
    success_url=reverse_lazy('listar_alimento')

    def test_func(self):
        user = self.request.user
        return user.has_perm('app_name.change_alimento')
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para editar alimentos.')
        return redirect('listar_alimento')

    def form_valid(self, form):
        messages.success(self.request, 'Alimento editado correctamente')
        return super().form_valid(form)
    

class BorrarAlimento(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model=Alimento
    template_name='contador_cal/Alimento_Borrar.html'
    success_url=reverse_lazy('listar_alimento')

    def test_func(self):
        user = self.request.user
        return user.has_perm('app_name.delete_alimento')
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para borrar alimentos.')
        return redirect('listar_alimento')
    
    def form_valid(self, form):
        messages.success(self.request, 'Alimento eliminado correctamente')
        return super().form_valid(form)



class RegistraPerfilUsuario(CreateView):
    form_class=Perfil_Usuario
    template_name='registration/registrarPerfil.html'

    def get_success_url(self):
        return reverse_lazy('registrar_Datos', kwargs={'pk': self.object.pk})

class RegistraDatosUsuario(UpdateView):
    model=Usuario
    form_class=Ficha_Usuario
    template_name='registration/registrarDatos.html'
    success_url=reverse_lazy('home')
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['action']='update'
        return context
    
    def form_valid(self, form):
        with transaction.atomic(): 
            # Guarda el usuario y obtiene el objeto actualizado
            usuario = form.save()

            # Marca el perfil como completado
            usuario.perfil_completado = True
            usuario.save()  # No olvides guardar los cambios del perfil

            # Crea un objeto Peso para el usuario
            Pesos.objects.create(usuario=usuario, peso=usuario.peso)

            # Inicia sesión al usuario
            login(self.request, usuario)
        return super().form_valid(form)


def cancelar_Registro(request):
    users = Usuario.objects.filter(perfil_completado=False).exclude(is_staff=True)
    users.delete()
    return redirect ('home')

class EditarFichaUsuario(LoginRequiredMixin, UpdateView):
    model = Usuario
    form_class =  Ficha_Usuario
    template_name='contador_cal/editarFichaUsuario.html'
    success_url=reverse_lazy('home')

    
class EditarPerfilUsuario(LoginRequiredMixin, TemplateView):

    def get(self, request, pk):
        usuario=get_object_or_404(Usuario, pk=pk)
        return render(request, 'contador_cal/editarPerfilUsuario.html', {'usuario': usuario})
    
    def post(self, request, pk):
        usuario=get_object_or_404(Usuario, pk=pk)
        usuario.username = request.POST.get('username')
        usuario.email = request.POST.get('email')
        usuario.first_name = request.POST.get('first_name')
        usuario.last_name = request.POST.get('last_name')

        usuario.save()

        return redirect('home')

class AñadirAlimento(LoginRequiredMixin, TemplateView):

    def get(self, request, pk):
        alimento=get_object_or_404(Alimento, pk=pk)
        return render(request, 'contador_cal/Alimento_Añadir.html', {'alimento': alimento})
    
    def post(self, request, pk):
        usuario = Usuario.objects.get(id=self.request.user.id)
        calorias = float(request.POST.get('calorias'))
        diario_existente = Diario.objects.filter(usuario=usuario, fecha=date.today()).first()
        
        if diario_existente:
            diario_existente.calorias += calorias
            diario_existente.save()
        else:
            Diario.objects.create(usuario=usuario, calorias=calorias)

        return redirect('home')
        
class Pesos_lista(LoginRequiredMixin, TemplateView):
    template_name = 'contador_cal/Peso_Listado.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = Usuario.objects.get(id=self.request.user.id)
        pesos = Pesos.objects.filter(usuario=usuario).all()
        paginacion = Paginator(pesos, 5)

        numero_pagina = self.request.GET.get('page')
        page_obj = paginacion.get_page(numero_pagina)


        context['page_obj'] = page_obj
        return context

class Guardar_peso(LoginRequiredMixin, TemplateView):
    template_name = 'contador_cal/Peso_Crear.html'

    def post(self, request):
        usuario = Usuario.objects.get(id=self.request.user.id)
        nuevo_peso = float(request.POST.get('nuevo_peso'))

        Pesos.objects.create(usuario=usuario, peso=nuevo_peso)
        usuario.peso=nuevo_peso
        usuario.save()
        return redirect('home')
        
        


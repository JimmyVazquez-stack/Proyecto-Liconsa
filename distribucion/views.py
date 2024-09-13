from django.shortcuts import render
from distribucion.models import EncabOrdenDesp, OrdenDespPNC
from distribucion.forms import EncabOrdenDespForm, OrdenDespForm
from django.views import generic 
from django.urls  import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView, DeleteView, FormView

#Index de la aplicación
class index(LoginRequiredMixin,TemplateView, PermissionRequiredMixin):
    model = get_user_model()
    template_name = 'index.html'
    login_url = reverse_lazy('usuarios:login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_usuarios'] = self.model.objects.exclude(is_staff=True).count()
        
        # Verifica si el usuario tiene el permiso directamente o a través de sus grupos
        permiso_nombre = 'usuario.add_usuario'
        tiene_permiso = self.request.user.has_perm(permiso_nombre) or \
                        self.request.user.groups.filter(permissions__codename=permiso_nombre.split('.')[1]).exists()
        context['puede_agregar_usuario'] = tiene_permiso
        return context

#[INICIO] CRUD Orden Despacho PNC ---------------------------------------------------
#[INICIO]ENCABEZADO---------------------------------------------------------------

class EncabOrdenDespListView(generic.ListView):
    model = EncabOrdenDesp
    queryset = EncabOrdenDesp.objects.all()
    template_name = 'OrdenDespachoPNC/encabOrdenDesp_List.html'
    context_object_name = 'encabOrdenDespContext'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EncabOrdenDespForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = EncabOrdenDespForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('distribucion:encabOrdenDesp_List')
        else:
            print("Form errors:", form.errors)  # Agrega esta línea para ver los errores del formulario
        return self.get(request, *args, **kwargs)

class EncabOrdenDespUpdateView(generic.UpdateView):
    model = EncabOrdenDesp
    template_name = 'OrdenDespachoPNC/encabOrdenDesp_Create.html'
    context_object_name = 'encabOrdenDespContext'
    form_class = EncabOrdenDespForm
    success_url = reverse_lazy("distribucion:encabOrdenDesp_List")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        encab_object = self.get_object()
        context['ordenDespContext'] = OrdenDespPNC.objects.filter(encabezado=encab_object)

        # Si se recibe un ID en el GET, se está editando un registro; de lo contrario, es un nuevo registro.
        ordenDespContext_id = self.request.GET.get('ordenDespContext_id')
        if ordenDespContext_id:
            try:
                ordenDespContext_instance = OrdenDespPNC.objects.get(id=ordenDespContext_id)
                nuevo_form = OrdenDespForm(instance=ordenDespContext_instance)
                context['edit_mode'] = True
            except OrdenDespPNC.DoesNotExist:
                nuevo_form = OrdenDespForm(initial={'encabezado': encab_object})
                context['edit_mode'] = False
        else:
            nuevo_form = OrdenDespForm(initial={'encabezado': encab_object})
            context['edit_mode'] = False

        nuevo_form.fields['encabezado'].widget.attrs['readonly'] = True
        context['form'] = self.get_form()
        context['nuevo_form'] = nuevo_form
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        ordenDespContext_id = request.POST.get('ordenDespContext_id')

        # Crear nuevo formulario de producto_terminado dependiendo de si es una edición o creación
        if ordenDespContext_id and ordenDespContext_id.isdigit():
            try:
                ordenDespContext_instance = OrdenDespPNC.objects.get(id=ordenDespContext_id)
                nuevo_form = OrdenDespForm(request.POST, instance=ordenDespContext_instance)
            except OrdenDespPNC.DoesNotExist:
                nuevo_form = OrdenDespForm(request.POST)
        else:
            nuevo_form = OrdenDespForm(request.POST)

        # Guardar el formulario de encabezado si se presionó su botón de guardar
        if 'submit-encab-form' in request.POST and form.is_valid():
            form.save()
            return redirect(self.success_url)

        # Guardar el formulario de orden Despacho si se presionó su botón de guardar
        if 'submit-nuevo-form' in request.POST and nuevo_form.is_valid():
            nuevo_form.save()
            return redirect(request.path)

        # En caso de errores, renderizar los formularios con los datos ya ingresados
        context = self.get_context_data()
        context['form'] = form
        context['nuevo_form'] = nuevo_form
        return self.render_to_response(context)
    
class EncabOrdenDespDeleteView(generic.DeleteView):
    model = EncabOrdenDesp
    template_name = 'OrdenDespachoPNC/encabOrdenDesp_Delete.html'
    context_object_name = 'encabOrdenDespContext'
    success_url = reverse_lazy("distribucion:encabOrdenDesp_List")

#[FIN]ENCABEZADO----------------------------------------------------------------------

#CRUD Orden Despacho
class OrdenDespListView(generic.ListView): 
    model = OrdenDespPNC
    queryset = OrdenDespPNC.objects.all()
    template_name = 'OrdenDespachoPNC/encabOrdenDesp_List.html'
    context_object_name = 'ordenDespContext'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OrdenDespForm()
        context['encab'] = EncabOrdenDespForm()
        return context

    def post(self, request, *args, **kwargs):
        ordform = OrdenDespForm(request.POST)
        encabform = EncabOrdenDespForm(request.POST)

        if ordform.is_valid() and encabform.is_valid():
            ordform.save()
            encabform.save()
            return redirect('distribucion:ordenDesp_List')
        else:
            # Mostrar errores de ambos formularios si hay alguno
            if ordform.errors:
                print("OrdenDespForm errors:", ordform.errors)
            if encabform.errors:
                print("EncabOrdenDespForm errors:", encabform.errors)
            
            # Si hay errores, volvemos a renderizar la vista con los formularios y errores
            return self.render_to_response(self.get_context_data(
                form=ordform, encab=encabform))


class OrdenDespCreateView(generic.CreateView):
    model = OrdenDespPNC
    template_name = 'OrdenDespachoPNC/encabOrdenDesp_Create.html'
    context_object_name = 'ordenDespContext'
    form_class = OrdenDespForm
    success_url = reverse_lazy("distribucion:ordenDesp_List")

class OrdenDespUpdateView(generic.UpdateView):
    model = OrdenDespPNC
    template_name = 'OrdenDespachoPNC/encabOrdenDesp_Create.html'
    context_object_name = 'ordenDespContext'
    form_class = OrdenDespForm
    success_url = reverse_lazy("distribucion:ordenDesp_List")
    

class OrdenDespDeleteView(generic.DeleteView):
    model = OrdenDespPNC
    template_name = 'OrdenDespachoPNC/encabOrdenDesp_Delete.html'
    context_object_name = 'ordenDespContext'
    success_url = reverse_lazy("distribucion:ordenDesp_List")

#[FIN] CRUD Orden Depacho PNC -------------------------------------------------------

from django.contrib.auth.mixins import LoginRequiredMixin 
from django.views import generic

# Create your views here.
# LoginRequiredMixin, generic.TemplateView

class Producto_no_Conforme_Home(generic.TemplateView):
    template_name = 'Prod_No_Conforme_Home.html'
    #login_url = 'login'

class Producto_no_Conforme_Registro(generic.TemplateView):
    template_name = 'Reg_Prod_No_Conforme.html'
    #login_url = 'login'
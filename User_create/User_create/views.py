from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, CreateView, ListView, FormView, UpdateView
from django.utils.text import capfirst
from django.urls import reverse
from django.forms.utils import ErrorList
from django.contrib.auth.mixins import LoginRequiredMixin

from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator


from DB.models import *
from .forms import *
from .send_mail import enviar_correo_activacion, send_mail_client

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from datetime import datetime
from django.db.models.functions import Coalesce
from django.db.models import Sum

from .choices import gender
########################################################################

class LoginView(LoginView):
    template_name = 'login.html'  

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')  
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Inicio de sesion"

        return context

class UserCreate(CreateView):
    model = Users
    form_class = UserCreateForm
    template_name = 'register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.first_name = capfirst(form.instance.first_name)
        form.instance.last_name = capfirst(form.instance.last_name)
        form.instance.is_active = False
        usuario = form.save(commit=False)
        usuario.save()
        enviar_correo_activacion(usuario, self.request)

        if form.errors:
            self.object = None
            errors = form.errors.get_json_data(escape_html=True)
            for field, field_errors in errors.item():
                form.add_error(field, ErrorList(field_errors))
            return self.render_ro_response(self.get_context_data(form=form))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('success_register')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro de usuario'

        return context

class UserActivate(TemplateView):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            usuario = Users.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            usuario = None

        if usuario is not None and default_token_generator.check_token(usuario, token):
            usuario.is_active = True
            usuario.save()
            return redirect('login')
        else:
            print(uid, usuario)
            return redirect('register')

class IndexView(TemplateView):
    template_name = "index.html"
    model = Client

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'graph_bars_ano':
                data = [{
                    'name': datetime.now().year,
                    'data': self.graph_bars_ano()
                },{
                    'name': datetime.now().year-1,
                    'data': self.graph_bars_ano2()
                },]
            elif action == 'graph_pie_gender':
                data = {
                    'name': 'According to gender',
                    'data': self.graph_pie_gender()
                }
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            return redirect('client_list')
        return JsonResponse(data, safe=False)


    def graph_pie_gender(self):
        data = []
        gender_choices = gender
        for i in gender_choices:
            total = Client.objects.filter(gender=i[0]).aggregate(
                r=Coalesce(Sum('sales'), 0)).get('r')
            data.append({
                'name': i[1],
                'y': float(total),
            })
        print(gender_choices)
        return data

    def graph_bars_ano(self):
        data = []
        year = datetime.now().year
        for month in range(1, 13):
            total = Client.objects.filter(date_create__year=year, date_create__month=month).aggregate(
                r=Coalesce(Sum('sales'), 0)).get('r')
            data.append(float(total))
        return data

    def graph_bars_ano2(self):
        data = []
        year = datetime.now().year-1
        for month in range(1, 13):
            total = Client.objects.filter(date_create__year=year, date_create__month=month).aggregate(
                r=Coalesce(Sum('sales'), 0)).get('r')
            data.append(float(total))
        return data

    
class SuccessRegister(TemplateView):
    template_name = "success_register.html"

class ClientRegister(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'form_client.html'

    def form_valid(self, form):
        usuario = self.request.user
        form.instance.name = capfirst(form.instance.name)
        form.instance.gender = capfirst(form.instance.gender)
        client = form.save(commit=False)
        client.save()
        send_mail_client(client, usuario)

        return redirect('client_register')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["title"] = "Client register"
        context["action"] = "add"

        return context


class ClientList(LoginRequiredMixin,ListView):
    model = Client
    template_name = "client_list.html"


    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                client = Client()
                client.name = request.POST['name']
                client.gender = request.POST['gender']
                client.dni = request.POST['dni']
                client.save()
            elif action == 'edit':
                client = Client.objects.get(pk=request.POST['id'])
                client.name = request.POST['name']
                client.gender = request.POST['gender']
                client.dni = request.POST['dni']
                client.save()
                return redirect('client_list')
            elif action == 'delete':
                client = Client.objects.get(pk=request.POST['id'])
                client.delete()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            return redirect('client_list')
        return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = Client.objects.all()
        context['formAdd'] = ClientForm()
        context['formEdit'] = ClientForm()

        context['title'] = "Register list"
        return context


class UserEdit(LoginRequiredMixin, UpdateView):
    model = Users
    form_class = UserEditForm
    template_name = 'useredit.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.username != request.user.username:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.first_name = capfirst(form.instance.first_name)
        form.instance.last_name = capfirst(form.instance.last_name)
        form.instance.address = capfirst(form.instance.address)
        form.instance.country = capfirst(form.instance.country)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'User edit'

        return context


class PasswordEdit(LoginRequiredMixin, FormView):
    model = Users
    form_class = PasswordChangeForm
    template_name = 'password_edit.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = PasswordChangeForm(user=self.request.user)
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        form = PasswordChangeForm(user=request.user, data=request.POST)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('login')
        else:
            data['error'] = form.errors

        return render(request, "password_edit.html", {"form": form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edicion de contraseña'

        return context

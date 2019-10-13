from django.shortcuts import render
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Avg, Max, Min, Sum
from django.db.models import Count
from .models import Category, Institution, Donation, TYP
from .forms import RegisterForm, LoginForm

# Create your views here.
class BaseView(View):
    def get(self, request):
        fundacje = Institution.objects.filter(typ=0)
        kat = Institution.categories.all()
        organizacje = Institution.objects.filter(typ=1)
        #kat2 = organizacje.categories.all()
        zbiorki = Institution.objects.filter(typ=2)
        #kat3 = zbiorki.categories.all()
        ctx = {
            "fundacje" : fundacje,
            "organizacje": organizacje,
            "zbiorki": zbiorki,
            "kat": kat
            # "kat2": kat2,
            # "kat3": kat3
        }
        return TemplateResponse(request, 'base.html', ctx)

class IndexView(View):
    def get(self, request):
        worki = list(Donation.objects.all().aggregate(Sum('quantity')).values())[0]
        fundacje = Institution.objects.count()
        return render(request, 'index.html', context={'worki':worki, 'fundacje':fundacje})
        
class FormConfView(View):
    def get(self, request):
        return TemplateResponse(request, 'form-confirmation.html')

class FormView(View):
    def get(self, request):
        return TemplateResponse(request, 'add-donation.html')

# class RegisterView(CreateView):
#     template_name = 'register.html'
#     model = User
#     fields = ['first_name', 'last_name', 'email', 'password']
#     success_url = "index"
class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return TemplateResponse(request, 'register.html', context={'form':form})
    def post(self, request):
        form = RegisterForm(request.POST)
        error = []
        if form.is_valid():
            print('form is valid')
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password_again = form.cleaned_data['password_again']
            if not User.objects.filter(email=email).exists():
                if password == password_again:
                    form.save()
                    User.objects.create(first_name=first_name, last_name=last_name, email=email, password=password)
                    return HttpResponseRedirect("index")
                else:
                    error.append('Hasła są różne')
            else:
                error.append('użytkownik isnieje')
        return render(request, 'register.html', cotext={'form':form, 'error':error})

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return TemplateResponse(request, 'login.html', context={'form':form})
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email, password = form.cleaned_data.values()
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return TemplateResponse(request, 'index.html')
            else:
                return HttpResponseRedirect("register")
        return TemplateResponse(request, 'login.html', context={'form':form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("index")
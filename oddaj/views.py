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
from .forms import RegisterForm, LoginForm, AddDonationForm

# Create your views here.
class BaseView(View):
    def get(self, request):
        #kat = Institution.categories.all()
        fundacje = Institution.objects.filter(typ="fundacja")
        organizacje = Institution.objects.filter(typ="organizacja pozarządowa")
        #kat2 = organizacje.categories.all()
        zbiorki = Institution.objects.filter(typ="zbiórka lokalna")
        #kat3 = zbiorki.categories.all()
        ctx = {
            "fundacje" : fundacje,
            "organizacje": organizacje,
            "zbiorki": zbiorki,
            # "kat": kat
            # "kat2": kat2,
            # "kat3": kat3
        }
        return TemplateResponse(request, 'base.html', ctx)

class IndexView(View):
    def get(self, request):
        worki = list(Donation.objects.all().aggregate(Sum('quantity')).values())[0]
        wszystkie = Institution.objects.count()
        return render(request, 'index.html', context={'worki':worki, 'wszystkie':wszystkie})
        
class FormConfView(View):
    def get(self, request):
        return TemplateResponse(request, 'form-confirmation.html')

class FormView(View):
    def get(self, request):
        form = AddDonationForm()
        return TemplateResponse(request, 'add-donation.html', context={'form':form})
    def post(self, reguest):
        form = AddDonationForm(request.POST)
        if form.is_valid():
            categories = form.cleaned_data['categories']
            quantity = form.cleaned_data['quantity']
            institution = form.cleaned_data['institution']
            adress = form.cleaned_data['adress']
            city = form.cleaned_data['city']
            zip_code = form.cleaned_data['zip_code']
            phone_number = form.cleaned_data['phone_number']
            pick_up_date = form.cleaned_data['pick_up_date']
            pick_up_time = form.cleaned_data['pick_up_time']
            pick_up_comment = form.cleaned_data['pick_up_comment']
            form.save()
            Donation.objects.create(categories=categories, quantity=quantity,  \
                institution=institution, adress=adress, city=city, zip_code=zip_code,  \
                phone_number=phone_number, pick_up_date=pick_up_date,  \
                pick_up_time=pick_up_time, pick_up_comment=pick_up_comment)
            return HttpResponse("OK")
        else:
            return TemplateResponse(request, 'add-donation.html', context={'form':form})

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
            username= form.cleaned_data['username']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            if not User.objects.filter(username=username).exists():
                if password == password2:
                    form.save()
                    User.objects.create_user(username, password, first_name=first_name, last_name=last_name)
                    return HttpResponseRedirect("index")
                else:
                    error.append('Hasła są różne')
            else:
                error.append('użytkownik isnieje')
#  return render(request, 'register.html', cotext={'form':form, 'error':error})

class LoginView(View):
     def get(self, request):
         form = LoginForm()
         return TemplateResponse(request, 'login.html', context={'form':form})
     def post(self, request):
         form = LoginForm(request.POST)
         if form.is_valid():
             username, password = form.cleaned_data.values()
             user = authenticate(username=username, password=password)
             if user is not None:
                 login(request, user)
                 return HttpResponseRedirect("index")
             else:
                 return HttpResponseRedirect("register")
         return TemplateResponse(request, 'login.html', context={'form':form})

# class LoginView(View):
#     def get(self, request):
#         return render(request, 'login.html')
#     def post(self, request):
#         username = request.POST.get('username', '')
#         password = request.POST.get('password', '')
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect("index")
#         else:
#             return redirect("register")

class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("index")
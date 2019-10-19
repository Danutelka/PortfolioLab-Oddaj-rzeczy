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
from .forms import LoginForm, AddDonationForm, RegisterUserForm

# Create your views here.
class BaseView(View):
    def get(self, request):
        fundacje = Institution.objects.filter(typ="fundacja")
        organizacje = Institution.objects.filter(typ="organizacja pozarządowa")
        zbiorki = Institution.objects.filter(typ="zbiórka lokalna")
        ctx = {
            "fundacje" : fundacje,
            "organizacje": organizacje,
            "zbiorki": zbiorki,
        }
        return TemplateResponse(request, 'base.html', ctx)

class IndexView(View):
    def get(self, request):
        worki = list(Donation.objects.all().aggregate(Sum('quantity')).values())[0]
        wszystkie = Institution.objects.count()
        fundacje = Institution.objects.filter(typ="fundacja")
        organizacje = Institution.objects.filter(typ="organizacja pozarządowa")
        zbiorki = Institution.objects.filter(typ="zbiórka lokalna")
        ctx = {
            "worki": worki,
            "wszystkie":wszystkie,
            "fundacje" : fundacje,
            "organizacje": organizacje,
            "zbiorki": zbiorki,
        }
        return render(request, 'index.html', ctx)
        
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
            z = Donation.objects.create(categories=categories, quantity=quantity,  \
                institution=institution, adress=adress, city=city, zip_code=zip_code,  \
                phone_number=phone_number, pick_up_date=pick_up_date,  \
                pick_up_time=pick_up_time, pick_up_comment=pick_up_comment)
            z.save()
            return HttpResponse("OK")
        else:
            return TemplateResponse(request, 'add-donation.html', context={'form':form})

class RegisterUserView(View):
    def get(self, request):
        form = RegisterUserForm()
        return render(request, 'register.html', context={'form':form})
    def post(self,request):
        form = RegisterUserForm(request.POST)
        error = []
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password_again = form.cleaned_data['password_again']
            email = form.cleaned_data['email']
            if not User.objects.filter(username=username).exists():
                if password == password_again:
                    u = User.objects.create_user(username, password, email, first_name=first_name, last_name=last_name)
                    u.save()
                    return HttpResponseRedirect("index")
                else:
                    error.append('Hasła są różne')
            else:
                error.append('użytkownik isnieje')
        return render(request, 'register.html', context={'form':form, 'error':error})

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return TemplateResponse(request, 'login.html', context={'form':form})
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("index")
            else:
                return HttpResponseRedirect("register")
        return render (request, 'login.html', context={'form':form, "email": form.email, "password": form.password})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("index")

class ProfileView(View):
    def get(self, request, pk):
        user = User.objects.get(id=pk)
        dary = Donation.objects.filter(user=user).order_by('-pick_up_date')
        context = {
            "user": user,
            "dary": dary
            }
        return TemplateResponse(request, 'profile.html', context=context)


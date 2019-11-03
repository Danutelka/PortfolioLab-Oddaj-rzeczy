from django.shortcuts import render, redirect
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
from django.core.paginator import Paginator
from django.core.mail import send_mail, mail_admins
from .models import Category, Institution, Donation, TYP
from .forms import LoginForm, AddDonationForm, RegisterUserForm, PasswordForm, UserEditForm,  \
    ResetPasswordForm, ContactForm

# Create your views here.
class BaseView(View):
    def get(self, request):
        return TemplateResponse(request, 'base.html')

class IndexView(View):
    def get(self, request):
        worki = list(Donation.objects.all().aggregate(Sum('quantity')).values())[0]
        wszystkie = Institution.objects.count()
        fundacje = Institution.objects.filter(typ="fundacja")
        paginator = Paginator(fundacje, 3)
        organizacje = Institution.objects.filter(typ="organizacja pozarządowa")
        pag2 = Paginator(organizacje, 3)
        zbiorki = Institution.objects.filter(typ="zbiórka lokalna")
        pag3 = Paginator(zbiorki, 3)
        page = request.GET.get('page')
        fundacje = paginator.get_page(page)
        organizacje = pag2.get_page(page)
        zbiorki = pag3.get_page(page)
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

class FormView(LoginRequiredMixin, View):
    def get(self, request):
        form = AddDonationForm()
        return TemplateResponse(request, 'add-donation.html', context={'form':form})
    def post(self, request):
        print("post1")
        form = AddDonationForm(request.POST)
        if form.is_valid():
            print("form is valid")
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
            user = request.user
            x = Donation.objects.create(quantity=quantity,  \
                institution=institution, adress=adress, city=city, zip_code=zip_code,  \
                phone_number=phone_number, pick_up_date=pick_up_date,  \
                pick_up_time=pick_up_time, pick_up_comment=pick_up_comment, user=user)
            x.save()
            x.categories.add(categories)
            print("after save")
            return TemplateResponse(request, 'form-confirmation.html')
        else:
            for field in form:
                print(field, field.errors)
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
                    u = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
                    u.save()
                    return HttpResponseRedirect("/regconf")
                else:
                    error.append('Hasła są różne')
            else:
                error.append('użytkownik isnieje')
        return render(request, 'register.html', context={'form':form, 'error':error})

class RegisterConfView(View):
    def get(self, request):
        return TemplateResponse(request, 'register-confirmation.html')

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
        dary = Donation.objects.filter(user=user).order_by('-is_taken')
        context = {
            "user": user,
            "dary": dary
            }
        return TemplateResponse(request, 'profile.html', context=context)
    def post(self, request, pk):
        user = User.objects.get(id=pk)
        dary = Donation.objects.filter(user=user).order_by('-is_taken')


class PasswordView(View):
    def get(self, request, pk):
        form = PasswordForm()
        user = User.objects.get(id=pk)
        context = {
            "form": form,
            "user": user
            }
        return TemplateResponse(request, 'password.html', context=context)
    def post(self, request, pk):
        user = User.objects.get(id=pk)
        form = PasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            if user.password == password:
                form.save()
                return HttpResponseRedirect("/editprofile/<int:pk>")
            else:
                return HttpResponse("nieprawidłowe hasło")
        return render (request, 'password.html', context={'form':form, "user": user})

class EditProfileView(View):
    def get(self, request, pk):
        us = User.objects.get(id=pk)
        context = {
            "us": us
        }
        return TemplateResponse(request, 'edit-profile.html', context=context)

class ChangeNameView(View):
    def get(self, request, pk):
        form = UserEditForm()
        us = User.objects.get(id=pk)
        context = {
            "us": us,
            "form": form
        }
        return TemplateResponse(request, 'change-name.html', context=context)
    def post(self, request, pk):
        form = UserEditForm(request.POST)
        us = User.objects.get(id=pk)
        if form.is_valid():
            if form.cleaned_data['first_name'] is not None and form.cleaned_data['first_name'] != '' : 
                us.first_name =  form.cleaned_data['first_name']
            if form.cleaned_data['last_name'] is not None and form.cleaned_data['last_name'] != '' : 
                us.last_name =  form.cleaned_data['last_name']
            us.save()
            return HttpResponseRedirect("/index")
        else:
            return HttpResponse("coś poszło nie tak...")
        return render (request, 'change-name.html', context={'form':form, "us": us})

class ResetPasswordView(View):
    def get(self, request, pk):
        form = ResetPasswordForm()
        us = User.objects.get(id=pk)
        return render(request, 'reset_password.html', context={'form': form, 'us': us})
    def post(self, request, pk):
        form = ResetPasswordForm(request.POST)
        us = User.objects.get(id=pk)
        if form.is_valid():
            us.new_password = form.cleaned_data['new_password']
            us.new2_password = form.cleaned_data['new2_password']
            if us.new_password == us.new2_password:
                us.set_password(request.POST.get('new_password'))
                us.save()
            else:
                return HttpResponse("wszystkie hasła muszą być jednakowe")
        return HttpResponseRedirect('/profile/<int:pk>') # użyć reverse

class TestView(View):
    def get(self, request):
        form = AddDonationForm()
        return TemplateResponse(request, 'test.html', context={'form':form})
    def post(self, request):
        print ("udało sie nareszcie")
        return HttpResponse("Jabadaba du")

class ContactView(View):
    def get(self, request):
        form2 = ContactForm()
        return TemplateResponse(request, 'footer.html', context={'form2': form2})
    def post(self, request):
        print("hhhhhhhh")
        use = User.objects.filter(is_superuser=True)
        form2 = ContactForm(request.POST)
        if form.is_valid():
            for x in use:
                name = form.cleaned_data['name']
                #surname = form.cleaned_data['surname']
                message = form.cleaned_data['message']
                subject = "{} {} wysłał/a wiadomość".format(name, surname)
                from_email = form.cleaned_data['surname']
                #'kontakt@oddajrzeczy.pl'
                recipient_list = ['{}'.format(x.email)]
            # send email code goes here
            #mail_admins('Kontakt', message)
                send_mail(subject, message, from_email, recipient_list, fail_silently=True)
                mail.send()
        else:
            return redirect(reverse('/index'))
        return TemplateResponse(request, 'form-confirmation.html', {'form': form})
        #     return render(request, 'contact-ans.html')
        # else:
        #     return TemplateResponse(request, 'contact.html', context={'form2': form2})
        # #return TemplateResponse(request, 'contact', {'form': form} 

class AnswerContView(View):
    def get(self, request):
        return render(request, 'contact-answer.html')
    def post(self, request):
        #print ("udało sie nareszcie")
        return render(request, 'contact-answer.html')
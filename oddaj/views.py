from django.shortcuts import render
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.conf.urls.static import static

# Create your views here.

class IndexView(View):
    def get(self, request):
        return TemplateResponse(request, 'index.html')

class FormConfView(View):
    def get(self, request):
        return TemplateResponse(request, 'form-confirmation.html')

class FormView(View):
    def get(self, request):
        return TemplateResponse(request, 'form.html')

class LoginView(View):
    def get(self, request):
        return TemplateResponse(request, 'login.html')

class RegisterView(View):
    def get(self, request):
        return TemplateResponse(request, 'register.html')
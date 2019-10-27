"""PortfolioLab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from oddaj.views import IndexView, FormConfView, FormView, LoginView, LogoutView, BaseView,  \
    RegisterUserView, ProfileView, RegisterConfView, PasswordView, EditProfileView, ChangeNameView,  \
    ResetPasswordView, TestView

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('', BaseView.as_view(), name="base"),
    path('index', IndexView.as_view(), name="index"),
    path('test', TestView.as_view(), name="test"),
    path('formconf', FormConfView.as_view(), name="form-conf"),
    path('form', FormView.as_view(), name="form"),
    path('login', LoginView.as_view(), name="login"),
    path('register', RegisterUserView.as_view(), name="register"),
    path('regconf', RegisterConfView.as_view(), name="reg-conf"),
    path('logout', LogoutView.as_view(), name="userlogout"),
    path('profile/<int:pk>', ProfileView.as_view(), name="profil"),
    path('pass/<int:pk>', PasswordView.as_view(), name="password"),
    path('editprofile/<int:pk>', EditProfileView.as_view(), name="edit-profile"),
    path('changename/<int:pk>', ChangeNameView.as_view(), name="change-name"),
    path('changepass/<int:pk>', ResetPasswordView.as_view(), name="change-pass")

]

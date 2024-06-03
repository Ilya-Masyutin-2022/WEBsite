from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View

from users.forms import LoginUserForm, RegisterUserForm


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': "Авторизация"}

    # def get_success_url(self):
    #     return reverse_lazy('home')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')


def register(request):
    form = RegisterUserForm()
    return render(request, 'users/register.html',
                  {'form': form})

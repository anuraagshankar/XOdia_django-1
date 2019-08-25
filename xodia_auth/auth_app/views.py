# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from models import User
from django.views.generic import View
from django.db.utils import IntegrityError

# Create your views here.
class HomeView(View):
    template_name = 'auth_app/index.html'
    def get(self, request):
        return render(request, self.template_name)

class LoginView(View):
    template_name = 'auth_app/login.html'
    def get(self, request):
        if request.user.is_authenticated():
            user = request.user.username
            return render(request, 'auth_app/success.html', {'username': user})
        else:
            return render(request, self.template_name)

    def post(self, request):
        context ={}
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('login_success'))
        else:
            context["error"] = "Incorrect Credentials!"
            return render(request, self.template_name, context)

class LogoutView(View):
    def post(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('user_login'))

class SuccessView(View):
    template_name = 'auth_app/success.html'
    def get(self, request):
        context = {}
        context['user'] = request.user
        return render(request, self.template_name, context)

class RegisterView(View):
    template_name = 'auth_app/register.html'

    def post(self, request):
        if request.POST['password'] == request.POST['password2'] :
            try:
                user = User()
                user.username = request.POST['username']
                user.set_password(request.POST['password'])
                user.save()
                login(request, user)

            except IntegrityError:
                context={'error': 'Username already exists'}
                return render(request, self.template_name, context)

            return HttpResponseRedirect(reverse('user_profile'))
        else:
            return render(request, self.template_name, {"error":"Passwords do not match!"})

    def get(self, request):
        return render(request, self.template_name)

class ProfileView(View):
    template_name = 'auth_app/profile.html'

    def post(self, request):
        user = request.user
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        if request.POST['college_name'] != "" :
            user.profile.college_name = request.POST['college_name']
        if request.POST['bio'] != "" :
            user.profile.bio = request.POST['bio']
        user.save()
        return HttpResponseRedirect(reverse('user_login'))

    def get(self, request):
        return render(request, self.template_name)
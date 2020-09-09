from typing import re

from django.shortcuts import render, get_object_or_404
# from requests import models

from .MyForms import RegistrationForm, LoginForm, ProfileForm
from .models import UserProfile
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    print("index doing")
    return HttpResponse("index OK")


@login_required
def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = ProfileForm(request.POST)

        if form.is_valid():
            user.email = form.cleaned_data['email']
            user.save()

            return HttpResponseRedirect(reverse('FirstApp:profile', args=[user.id]))
    else:
        default_data = {'email': user.email, }
        form = ProfileForm(default_data)
    return render(request, 'users/profile.html', {'form': form, 'user': user})


# @login_required
# def profile_update(request, pk):
#     user = get_object_or_404(User, pk=pk)
#     # user_profile = get_object_or_404(UserProfile, user=user)
#
#     if request.method == 'POST':
#         form = ProfileForm(request.POST)
#
#         if form.is_valid():
#             user.email = form.cleaned_data['email']
#             user.save()
#
#             return HttpResponseRedirect(reverse('FirstApp:profile', args=[user.id]))
#     else:
#         default_data = {'email': user.email, }
#         form = ProfileForm(default_data)
#
#     return render(request, 'users/profile_update.html', {'form': form, 'user': user})


def register(request):
    if request.method == 'POST':

        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']

            user = User.objects.create_user(username=username, password=password, email=email)

            user_profile = UserProfile(user=user)
            user_profile.save()

            return HttpResponseRedirect("/FirstApp/login/")
    else:
        form = RegistrationForm()
    return render(request, 'users/registration.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('FirstApp:profile', args=[user.id]))
            else:
                return render(request, 'users/login.html',
                              {'form': form, 'message': 'Mot de passe incorrect, veuillez réessayer'})
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/FirstApp/login/")


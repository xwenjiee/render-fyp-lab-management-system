from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm
from django.contrib import messages

# Create your views here.


def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/logout/")
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Account created successfully. Please log in.")
            return redirect("user-login")
    else:
        form = CreateUserForm()
    context = {"form": form}
    return render(request, "user/register.html", context)


@login_required(login_url="user-login")
def profile(request):
    context = {}
    return render(request, "user/profile.html", context)


@login_required(login_url="user-login")
def password_update(request):
    form = PasswordChangeForm(user=request.user)

    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            logout(request)
            return HttpResponseRedirect("/logout/")

    context = {
        "u_form": form,
    }

    return render(request, "user/password_update.html", context)

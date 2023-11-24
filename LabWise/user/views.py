from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm

# Create your views here.


def register(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            # group = Group.objects.get(name="Customers")
            # user.groups.add(group)
            return redirect("user-login")
    else:
        form = CreateUserForm()
    context = {"form": form}
    return render(request, "user/register.html", context)


@login_required(login_url="user-login")
def profile(request):
    context = {}
    return render(request, "user/profile.html", context)


# def profile_update(request, username):
#     user = User.objects.get(username=username)
#     if request.method == "POST":
#         u_form = UserUpdateForm(request.POST, instance=user)
#         # p_form = ProfileUpdateForm(
#         #     request.POST, request.FILES, instance=request.user.profile
#         # )
#         if u_form.is_valid():
#             u_form.save()
#             # p_form.save()
#             return redirect("user-profile")
#     else:
#         u_form = UserUpdateForm(instance=user)
#         # p_form = ProfileUpdateForm(instance=request.user.profile)

#     context = {
#         "u_form": u_form,
#         # "p_form": p_form,
#     }
#     return render(request, "user/profile_update.html", context)


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
        # "p_form": p_form,
    }

    return render(request, "user/password_update.html", context)

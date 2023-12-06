from django.http import HttpResponse
from django.shortcuts import redirect


def auth_users(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard-index")
        else:
            return view_func(request, *args, **kwargs)

    return wrapper


def allowed_users(allowed_roles=[]):
    def decorators(view_func):
        def wrapper(request, *args, **kwargs):
            group = request.user.is_staff
            if group in allowed_roles:
                print("You are a staff")
                return view_func(request, *args, **kwargs)
            else:
                return redirect("dashboard-index")

        return wrapper

    return decorators


def superuseronly(allowed_roles=[]):
    def decorators(view_func):
        def wrapper(request, *args, **kwargs):
            group = request.user.is_superuser
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return redirect("dashboard-index")

        return wrapper

    return decorators

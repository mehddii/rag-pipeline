from django.shortcuts import render
from .forms import UserRegistrationForm, UserLoginForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            
            user.set_password(
                form.cleaned_data["password1"]
            )

            user.save()
            return HttpResponse("Registered successfully")
    else:
        form = UserRegistrationForm()

    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST) 

        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            ) 

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Authenticated successfully")
                else:
                    return HttpResponse("Disabled account")
            else:
                return HttpResponse("Invalid login")
    else:
        form = UserLoginForm()
    
    return render(request, "users/login.html", {"form": form})

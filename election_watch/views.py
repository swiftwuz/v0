from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from users.models import User
from mobile_api.models import Incident
from .forms import (
    UserUpdateForm, ProfileUpdateForm,
    AdminRegistrationForm, AdminLoginForm
)
from .models import Admin


def dashboard(request):
    return render(request, "election_watch/dashboard.html")


def feedback(request):
    return render(request, "election_watch/feedback.html")


def incidents(request):
    context = {
        "incident": Incident.objects.all()
    }
    return render(request, "election_watch/incidents.html", context)


def sign_in(request):
    if request.method == "POST":
        form = AdminLoginForm(request.POST)
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("incidents")
        else:
            messages.error(request, "Invalid email or password.")
    else:
        form = AdminLoginForm()
        return render(request, "election_watch/login.html",
                      {"form": form})


def reports(request):
    return render(request, "election_watch/reports.html")


def results(request):
    return render(request, "election_watch/results.html")


# def register_institution(request):
    # if request.method == "POST":
        # form = AdminRegistrationForm(request.POST)
        # if form.is_valid():
            # form.save()
            # name = form.cleaned_data.get("name")
            # form.cleaned_data.get("email")
            # form.cleaned_data.get("telephone")
            # form.cleaned_data.get("city")
            # form.cleaned_data.get("street")
            # form.cleaned_data.get("address_line")
            # messages.success(request,
                             # f"Institution created for {name}.")
            # return redirect("login")
    # else:
        # form = InstRegistrationForm()
        # return render(request, "election_watch/registration/institution.html",
                      # {"form": form})


def register_agents(request):
    return render(request, "election_watch/registration/agents.html")


def register_location(request):
    return render(request, "election_watch/registration/location.html")


def register_admin(request):
    if request.method == "POST":
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            email = form.cleaned_data.get("email")
            username = form.cleaned_data.get("username")
            new_user.set_password(form.cleaned_data["password"])
            new_user.save()
            Admin.objects.create(user=new_user, username=username, email=email)
            User.objects.filter(email=email).update(
                is_admin=True
            )

            messages.success(request,
                             f"Account created for {username}.")

            return redirect("login")
    else:
        form = AdminRegistrationForm()
        return render(request, "election_watch/index.html",
                      {"form": form})


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            messages.success(request, "Your account has been updated")
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

        context = {
            "u_form": u_form,
            "p_form": p_form,
        }
        return render(request, "election_watch/profile.html", context)

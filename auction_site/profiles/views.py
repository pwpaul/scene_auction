from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import ForcedPasswordChangeForm, ProfileForm


@login_required
def dashboard(request):
    return render(request, "profiles/dashboard.html")


@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("dashboard")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "profiles/edit_profile.html", {"form": form})


@login_required
def force_password_change(request):
    if request.method == "POST":
        form = ForcedPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            request.user.must_change_password = False
            request.user.save()
            messages.success(request, "Password changed successfully!")
            return redirect("dashboard")
    else:
        form = ForcedPasswordChangeForm(user=request.user)
    return render(request, "profiles/force_password_change.html", {"form": form})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib import messages
from .forms import ForcedPasswordChangeForm, ProfileForm
from scenes.models import Scene


@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profiles/edit_profile.html', {'form': form})
@login_required
def dashboard(request):
    profile = request.user.profile
    scenes = (
        Scene.objects.filter(profile=profile)
        .select_related("auction")
        .order_by("-auction__date")
    )
    has_scenes = scenes.exists()
    return render(
        request, "profiles/dashboard.html", {"scenes": scenes, "has_scenes": has_scenes}
    )


# @login_required
# def edit_profile(request):
#     profile = request.user.profile
#     if request.method == "POST":
#         form = ProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Profile updated successfully.")
#             return redirect("dashboard")
#     else:
#         form = ProfileForm(instance=profile)
#     return render(request, "profiles/edit_profile.html", {"form": form})

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=profile)

    if request.headers.get('Hx-Request'):
        html = render_to_string('profiles/_profile_form.html', {'form': form}, request)
        return HttpResponse(html)

    return render(request, 'profiles/edit_profile.html', {'form': form})


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


def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    return render(request, "public_home.html")

def faq(request):
    return render(request, 'faq.html')



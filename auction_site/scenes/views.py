from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Auction, Scene
from .forms import SceneForm
from profiles.models import Profile


@login_required
def auction_list(request):
    auctions = Auction.objects.order_by("-date")
    return render(request, "scenes/auction_list.html", {"auctions": auctions})


@login_required
def add_scene(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    profile = request.user.profile
    scene, created = Scene.objects.get_or_create(auction=auction, profile=profile)

    if request.method == "POST":
        form = SceneForm(request.POST, instance=scene)
        if form.is_valid():
            form.save()
            messages.success(request, "Your scene was saved!")
            return redirect("dashboard")
    else:
        form = SceneForm(instance=scene)

    return render(request, "scenes/scene_form.html", {"form": form, "auction": auction})

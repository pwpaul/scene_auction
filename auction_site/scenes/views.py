from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
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


@staff_member_required
def admin_scene_dashboard(request):
    scenes = (
        Scene.objects.select_related("auction", "profile__user")
        .prefetch_related("eligible_bidders")
        .order_by("auction__date", "profile__name")
    )

    return render(request, "scenes/admin_scene_dashboard.html", {"scenes": scenes})


@staff_member_required
def toggle_scene_ready(request, scene_id):
    scene = get_object_or_404(Scene, id=scene_id)
    scene.ready = not scene.ready
    scene.save()
    return redirect("admin_scene_dashboard")


@staff_member_required
def projection_view(request, scene_id, slug=None):
    scene = get_object_or_404(
        Scene.objects.select_related('profile__user', 'auction').prefetch_related('eligible_bidders'),
        id=scene_id
    )
    other_scenes = Scene.objects.filter(auction=scene.auction).order_by('order', 'profile__name')
    
    if request.headers.get("HX-Request"):
        html = render_to_string("scenes/_projection_content.html", {"scene": scene})
        return HttpResponse(html)
    
    return render(request, "scenes/projection.html", {"scene": scene, "other_scenes": other_scenes})

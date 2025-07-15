from django.db import models


class Auction(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    desc = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} on {self.date}"


class EligibleBidder(models.Model):
    code = models.CharField(max_length=20, unique=True)
    desc = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.code} ({self.desc})"


class Scene(models.Model):
    auction = models.ForeignKey(
        Auction, on_delete=models.CASCADE, related_name="scenes"
    )
    profile = models.ForeignKey(
        "profiles.Profile", on_delete=models.CASCADE, related_name="scenes"
    )

    role = models.CharField(
        max_length=10,
        choices=[("top", "Top"), ("bottom", "Bottom")],
        help_text="Your Role in the scene",
    )  # "Eligible Bidders (optional)",
    eligible_bidders = models.ManyToManyField(
        EligibleBidder,
        blank=True,
        verbose_name="Eligible Bidders (Select All That Apply - Optional)",
        help_text="This is an effort to make sure bidders are compatible in more sexually based scenes.<p> This is optional for scenes where sexual contact is not available.</p>",
    )
    other_bidders = models.CharField("Other Eligible Bidders",
        max_length=200,
        blank=True,
        help_text="Any other specific bidder audience not listed (I tried but you know better than I do).",
    )

    title = models.CharField(max_length=200, blank=False, help_text="This is the title the auctioneer will use for your scene")
    short = models.TextField("Short Scene Description", blank=False, help_text="Main description for the auctioneer and audience.<p> Please be explicit if sexual contact is included.  All contact is negotated before scene happens </p>")
    long = models.TextField("Long Scene Description", blank=True, help_text="Optional longer description, will help the auctioneer be more descriptive.")

    ready = models.BooleanField(default=False)
    order = models.PositiveIntegerField(
        default=0, help_text="Controls order in the projection dropdown."
    )

    class Meta:
        unique_together = ("auction", "profile")
        ordering = ["order", "profile__name"]  # default ordering

    def __str__(self):
        return f"{self.title} by {self.profile.user.username} in {self.auction.name}"

    def save(self, *args, **kwargs):
        if self._state.adding and self.order == 0:
            # find highest order for this auction and add 1
            last_scene = Scene.objects.filter(auction=self.auction).order_by('-order').first()
            self.order = (last_scene.order + 1) if last_scene else 1
        super().save(*args, **kwargs)

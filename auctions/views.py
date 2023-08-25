from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Category, Bid
from .forms import ListingForm


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    

def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        category = Category.objects.get(id=request.POST["category"])
        imageUrl = request.POST["imageUrl"]
        user = request.user

        l = Listing(title=title, description=description, starting_bid=starting_bid, current_price=starting_bid, category=category, imageUrl=imageUrl, user=user)
        l.save()

        return HttpResponseRedirect(reverse("index"))
    listing_form = ListingForm()
    return render(request, "auctions/create.html", {
        "form": listing_form
    })


def listing(request, id):
    listing = Listing.objects.get(id=id)
    listing_bids = listing.bids.all()
    if request.method == "POST":
        if request.POST["bid_amount"]:
            created_bid = Bid(listing_id = listing, bid_amount=float(request.POST["bid_amount"]), user=request.user)
            if listing_bids:
                if all(listing_bid.bid_amount < created_bid.bid_amount for listing_bid in listing_bids):
                    created_bid.save()
                    listing.current_price = created_bid.bid_amount
                    listing.save()
            else:
                if created_bid.bid_amount >= listing.starting_bid:
                    created_bid.save()
                    listing.current_price = created_bid.bid_amount
                    listing.save()

        elif request.POST["delete"]:
            listing.delete()


        return HttpResponseRedirect(reverse("listing", kwargs={'id': listing.id}))

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "price": max(listing_bids, key=lambda x: x.bid_amount).bid_amount if bool(listing_bids) else listing.starting_bid,
        "min_bid": max(listing_bids, key=lambda x: x.bid_amount).bid_amount+1 if bool(listing_bids) else listing.starting_bid,
        "delete_listing": bool(request.user == listing.user)
    })

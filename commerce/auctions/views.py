from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Listing, Watchlist, Bid, Comment, Category


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
    return HttpResponseRedirect(reverse("login"))


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


@login_required(login_url='/login/')
def create(request):
    if request.method == "POST":
        owner = User.objects.get(username=request.POST["owner"])
        title = request.POST["title"]
        description = request.POST["description"]
        category = request.POST["category"]
        image = request.POST["image"]
        price = request.POST["price"]
        date = datetime.now()
        try:
            listing = Listing(owner=owner, title=title, description=description, image=image, price=price, date=date, category=category)
            listing.save()
        except IntegrityError:
            return render(request, "auction/create.html", {
            "message": "Try again."
            })
        return redirect('listing', listing_title=title)
    else:
        return render(request, "auctions/create.html", {
        "owner":request.user, "categories":Category.objects.all()
        })



def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "watchlist":Watchlist.objects.filter(user=request.user)
        })


@login_required(login_url='/login/')
def listing(request,listing_title):
    try:
        bid = Bid.objects.get(listing__title=listing_title)
        no_bid = False
    except ObjectDoesNotExist:
        no_bid = True
        bid = None
    listing = Listing.objects.get(title=listing_title)
    comments = Comment.objects.filter(listing__title=listing_title)
    if request.method == "POST":

        try:
            #check if listing_title is already in Watchlist
            w = Watchlist.objects.get(user=request.user, listing=listing)
            # delete listing from watchlist
            w.delete()
            return render(request, "auctions/listing.html", {
            "listing":listing, "delete": False, "bid":bid, "no_bid":no_bid, "comments":comments
            })
        except ObjectDoesNotExist:
            #add listing to watchlist
            w = Watchlist.objects.create(user=request.user, listing=listing)
            w.save()
            return render(request, "auctions/listing.html", {
            "listing":listing, "delete": True, "bid":bid, "no_bid":no_bid, "comments":comments
            })
    else:
        try:
            # ist listing schon auf der Watchlist?
            w = Watchlist.objects.get(user=request.user, listing=listing)
            # listing muss entfernt werden können, via Button
            return render(request, "auctions/listing.html", {
            "listing":listing, "delete": True, "bid":bid, "no_bid":no_bid, "comments":comments
            })
        except ObjectDoesNotExist:
            return render(request, "auctions/listing.html", {
            "listing":listing, "delete": False, "bid":bid, "no_bid":no_bid, "comments":comments
            })


def bid(request,listing_title):
    if request.method == "POST":
        listing = Listing.objects.get(title=listing_title)
        comments = Comment.objects.filter(listing__title=listing_title)
        try:
            w = Watchlist.objects.get(user=request.user, listing__title=listing_title)
            delete = True
        except ObjectDoesNotExist:
            delete = False
        try:
            current_bid = int(request.POST["bid"])
        except ValueError:
            current_bid = 0

        try:
            existing_bid = Bid.objects.get(listing__title=listing_title)
            bid = existing_bid.bid
            if bid < current_bid:
                #wir wollen  Bid verändern
                existing_bid.user = request.user
                existing_bid.bid = current_bid
                existing_bid.save()
                return redirect('listing', listing_title=listing_title)
            else:
                return render(request, "auctions/listing.html", {
                "listing":listing, "delete":delete, "wrong_bid": True, "bid":Bid.objects.get(listing__title=listing_title), "comments":comments
                })
        except ObjectDoesNotExist:
            bid = listing.price
            if bid < current_bid:
                #wir wollen ein neuen Bid erstellen
                b = Bid.objects.create(listing=listing, user=request.user, bid=current_bid)
                b.save()
                return redirect('listing', listing_title=listing_title)
            else:
                return render(request, "auctions/listing.html", {
                "listing":listing, "delete":delete, "wrong_bid": True, "no_bid":True, "listing_price":Listing.objects.get(title=listing_title), "comments":comments
                })
    else:
        return HttpResponseRedirect(reverse("index"))


def close(request, listing_title):
    if request.method == "POST":
        listing = Listing.objects.get(title=listing_title)
        listing.active = False
        listing.save()
        listing = Listing.objects.get(title=listing_title)
        try:
            w = Watchlist.objects.get(user=request.user, listing__title=listing_title)
            delete = True
        except ObjectDoesNotExist:
            delete = False
        try:
            bid = Bid.objects.get(listing__title=listing_title)
            no_bid = False
        except ObjectDoesNotExist:
            no_bid = True
            bid = None
        return redirect('listing', listing_title=listing_title)


def comment(request, listing_title):
    if request.method == "POST":
        listing = Listing.objects.get(title=listing_title)
        user = request.user
        comment = request.POST["comment"]
        c = Comment.objects.create(listing=listing, user=user, comment=comment)
        c.save()
        return redirect('listing',listing_title=listing_title)
    else:
        return redirect('listing', listing_title=listing_title)




@login_required(login_url='login/')
def category(request):
    return render(request, "auctions/category.html", {
    "categories":Category.objects.all()
    })

@login_required(login_url='login/')
def category_listing(request, category):
    return render(request, "auctions/category_listing.html", {
    "listings": Listing.objects.filter(category=category), "category":category
    })

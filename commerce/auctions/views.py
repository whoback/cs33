from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import *


def index(request):
    # grab listings and display them
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {'listings': listings})


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


@login_required(login_url='/login/')
def create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        starting_bid = request.POST.get('bid')
        url = request.POST.get('url')
        listed_by = User.objects.get(username=request.user.username)
        listing = Listing(title=title, description=description,
                          starting_bid=starting_bid, image_url=url, listed_by=listed_by)
        listing.save()
        return redirect('/')

    return render(request, 'auctions/create.html')


@login_required(login_url='/login/')
def listing(request, id):
    user = User.objects.get(username=request.user.username)
    listing = Listing.objects.get(id=id)
    is_in_watchlist = Watchlist.objects.filter(listing_id=listing, user=user)
    watched = False
    try:
        watched = is_in_watchlist[0].watch_bool
    except:
        pass

    return render(request, 'auctions/listing.html', {'listing': listing, 'watched': watched})


@login_required(login_url='/login/')
def watchlist(request):
    user = request.user.username

    if request.method == 'POST':
        listing_id = request.POST.get('id')
        id = Listing.objects.get(id=listing_id)
        user = User.objects.get(username=user)
        is_in_watchlist = Watchlist.objects.filter(listing_id=id, user=user)
        if len(is_in_watchlist):
            is_in_watchlist.update(
                watch_bool=not is_in_watchlist[0].watch_bool)
        else:
            Watchlist(listing_id=id, user=user).save()

        return redirect(f'/listing/{listing_id}')
    watchlist = Watchlist.objects.filter(
        user=User.objects.get(username=user), watch_bool=True)
    listings = []
    for item in watchlist:
        listings.append(item.listing_id)
    print(listings)
    return render(request, 'auctions/watchlist.html', {'listings': listings})

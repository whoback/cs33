from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404

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
        categories = request.POST.get('categories')

        listing = Listing(title=title, description=description,
                          starting_bid=starting_bid, category=Category.objects.get(category=categories), image_url=url, listed_by=listed_by)
        listing.save()
        return redirect('/')
    categories = Category.objects.all()

    return render(request, 'auctions/create.html', {'categories': categories})


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
    bids = Bids.objects.filter(listing_id=id).count()
    comments = {}
    comments = Comment.objects.filter(listing_id=id)
    return render(request, 'auctions/listing.html', {'listing': listing, 'watched': watched, 'bids': bids, 'comments': comments})


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
    return render(request, 'auctions/watchlist.html', {'listings': listings})


@login_required(login_url='/login/')
def addcategory(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category = Category(category=name)
        category.save()
        return HttpResponseRedirect(reverse(create))
    return render(request, 'auctions/add_category.html')


def category(request, category_type=None):
    if category_type is None:
        category = Category.objects.all()
        return render(request, 'auctions/category.html', {'category': category})
    listings = Listing.objects.filter(
        category=Category.objects.get(category=category_type))

    return render(request, 'auctions/index.html', {'listings': listings})


@login_required(login_url='/login/')
def bid(request):
    if request.method == "POST":
        listing_id = request.POST.get('listing_id')
        new_bid = request.POST.get('bid')
        listing = Listing.objects.get(id=listing_id)
        cur_bid = listing.current_bid
        num_of_bids = Bids.objects.filter(listing_id=listing_id).count()
        if num_of_bids == 0:
            add_bid = Bids(user=User.objects.get(username=request.user.username),
                           bid=new_bid, listing_id=Listing.objects.get(id=listing_id))
            add_bid.save()

            return redirect(f'/listing/{listing_id}')
        if cur_bid == None:
            cur_bid = 0
        if float(new_bid) > float(cur_bid):
            add_bid = Bids(user=User.objects.get(username=request.user.username),
                           bid=new_bid, listing_id=Listing.objects.get(id=listing_id))
            add_bid.save()

            Listing.objects.filter(id=listing_id).update(current_bid=new_bid)

            return redirect(f'/listing/{listing_id}')
        else:
            raise Http404("Bid too low!")
    return HttpResponseRedirect(reverse("index"))


@login_required(login_url='/login/')
def add_comment(request):
    if request.method == "POST":
        listing_id = request.POST.get('listing_id')
        comment = request.POST.get('comment')
        user = request.user.username

        id = Listing.objects.get(id=listing_id)
        if len(Comment.objects.filter(comment_by=User.objects.get(username=user),
                                      listing_id=listing_id)):
            Comment.objects.filter(listing_id=id).update(
                comment=comment)

        else:
            comment = Comment(listing_id=id, comment=comment,
                              comment_by=User.objects.get(username=user))
            comment.save()

        return redirect(f'/listing/{listing_id}')

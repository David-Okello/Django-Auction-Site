from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db import models, transaction

from .models import User, Category, Item, Comments, Bids, WatchList, HighestBidder
from .forms import BidForm, CommentForm, ListingForm


def index(request):
    active_listings = Item.objects.filter(is_sold = False)
    return render(request, "auctions/index.html",{
        'active_listings': active_listings
    })

def view_watchlist(request):
    active_user = request.user
    watchlist_obj = WatchList.objects.filter(created_by=request.user).select_related('item')
    return render(request, 'auctions/watchlist.html',{
        'watchlist_obj':watchlist_obj,
        'active_user': active_user
    })

def view_categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/view_categories.html",{
        'categories': categories
    })

def category_details(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    active_listings = Item.objects.filter(category=category, is_sold=False)

    return render(request, 'auctions/category_details.html',{
        'category': category,
        'active_listings': active_listings
    })

def watchlist(request):
    if request.method == 'POST':
        listing_id = request.POST.get('listing_id')

        if 'add_button' in request.POST:
            # Check if the item is already in the WatchList
            if WatchList.objects.filter(item__pk=listing_id, created_by=request.user).exists():
                return HttpResponse("Item already in watchlist")
            else:
                item_add = get_object_or_404(Item, pk=listing_id)
                new_add = WatchList(item=item_add, created_by=request.user)
                new_add.save()
                return redirect('view_watchlist')
        elif 'remove_button' in request.POST:
            watchlist_entry = WatchList.objects.filter(item__pk=listing_id, created_by=request.user).first()
            if not watchlist_entry:
            # Handle the case where the item is not in the WatchList
                return HttpResponse("Item not in watchlist")
            else:
                watchlist_entry.delete()
                return redirect('view_watchlist')

def create_listing(request):
    if request.method == 'POST':
        new_item = ListingForm(request.POST, request.FILES)

        if new_item.is_valid():
            name = new_item.cleaned_data['name']
            description = new_item.cleaned_data['description']
            price = new_item.cleaned_data['price']
            image = new_item.cleaned_data['image']
            category = new_item.cleaned_data['category']

            neww = Item(name=name, description=description, price=price, image=image, is_sold=False, category=category, created_by=request.user)
            neww.save()

            return redirect('index')
        else:
            # Print form errors for debugging
            error_message = new_item.errors

            # Form is not valid, render the form with validation errors
            return render(request, 'auctions/create_listing.html', {
                'form': new_item,
                'error_message':error_message
                })
    else:
        new_item = ListingForm()
        return render(request, 'auctions/create_listing.html',{
            'form': new_item
        })

def listing(request, id):
    bid_form = BidForm()
    comment_form = CommentForm()
    listing = Item.objects.get(pk=id)
    listing_comments = Comments.objects.filter(item=listing)
    winner = HighestBidder.objects.filter(item=listing)

    can_close = True if listing.created_by == request.user else False

    if request.method == 'POST':
        bid_form = BidForm(request.POST)
        comment_form = CommentForm(request.POST)

        if 'close_listing_button' in request.POST:
            item_to_close = Bids.objects.filter(item=listing)
            highest_bid = item_to_close.aggregate(max_bid=models.Max('amount'))['max_bid']
            highest_bidder = Bids.objects.filter(amount=highest_bid).first().created_by

            with transaction.atomic():
                listing.is_sold = True
                listing.save()

            add_highest_bidder = HighestBidder(item=listing, highest_bidder=highest_bidder)
            add_highest_bidder.save()

            return redirect('index')

        if bid_form.is_valid():
            amount = bid_form.cleaned_data['bid_amount']
            
            # Create and save the new bid
            bid = Bids(amount=amount, item=listing, created_by=request.user)
            bid.save()

            # Redirect to a success page or the item details page
            return redirect('listing', id=listing.id)
        
        if comment_form.is_valid():
            title = comment_form.cleaned_data['title']
            commented = comment_form.cleaned_data['description']

            saved_comment = Comments(title=title, description=commented, item=listing, created_by=request.user)
            saved_comment.save()
            return redirect('listing', id=listing.id)

    else:
        return render(request, "auctions/listing.html",{
            "listing":listing,
            "listing_comments":listing_comments,
            'bid_form': bid_form,
            'comment_form':comment_form,
            'can_close': can_close,
            'winner': winner
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

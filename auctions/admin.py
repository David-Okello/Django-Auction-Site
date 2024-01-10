from django.contrib import admin

# Register your models here.
from .models import User, Category, Item, Comments, Bids, WatchList, HighestBidder

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Comments)
admin.site.register(Bids)
admin.site.register(WatchList)
admin.site.register(HighestBidder)
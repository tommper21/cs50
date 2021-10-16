from django.contrib import admin
from .models import Listing, Bid, User, Watchlist, Category, Comment

# Register your models here.
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(User)
admin.site.register(Watchlist)
admin.site.register(Category)
admin.site.register(Comment)

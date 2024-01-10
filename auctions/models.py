from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length = 255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
class Item(models.Model):
    name = models.CharField(max_length = 255)
    description = models.TextField(blank = True, null = True)
    price = models.FloatField()
    image = models.ImageField(upload_to = 'item_images')
    is_sold = models.BooleanField(default = False)
    category = models.ForeignKey(Category, related_name = 'items', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    created_by = models.ForeignKey(User, related_name = 'items', on_delete = models.CASCADE)

    def __str__(self):
        return self.name
    
class Comments(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    item = models.ForeignKey(Item, related_name = 'item_comment', on_delete = models.CASCADE)
    created_by = models.ForeignKey(User, related_name = 'comment', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f"{self.title} by {self.created_by.username}"
    
class Bids(models.Model):
    amount = models.FloatField(validators=[MinValueValidator(limit_value=0.01)])
    item = models.ForeignKey(Item, related_name='item_bids', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='bids', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Bids'

    def save(self, *args, **kwargs):
        # Set the minimum value of amount to the price of the associated item
        if not self.amount or self.amount < self.item.price:
            self.amount = self.item.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Bid on {self.item.name} by {self.created_by.username}"
    
class WatchList(models.Model):
    item = models.ForeignKey(Item, related_name="watchlist", on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name="user_watchlist", on_delete=models.CASCADE)

    def __str__(self):
        return f"Addition of {self.item.name} by {self.created_by.username} to their watchlist"
    
class HighestBidder(models.Model):
    item = models.ForeignKey(Item, related_name="highest_bidder", on_delete=models.CASCADE)
    highest_bidder = models.ForeignKey(User, related_name='highest_bidder', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.highest_bidder.username} is the highest bidder for {self.item.name}"
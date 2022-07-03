from django.db import models
from gems_shop.settings import AUTH_USER_MODEL
from store.models import Gem, Variation
from accounts.models import CustomAccount


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user = models.ForeignKey(CustomAccount, on_delete=models.CASCADE, null=True)
    gem = models.ForeignKey(Gem, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1, null=True)
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.gem.price * self.quantity

    def __unicode__(self):
        return self.gem
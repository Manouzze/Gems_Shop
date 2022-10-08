
from django.shortcuts import render, get_object_or_404

from carts.models import CartItem, Cart
from store.models import Gem
from category.models import Category
from carts.views import cart_id_session
from django.db.models import Q


def home(request):
    products = Gem.objects.all().filter(is_available=True)
    return render(request, 'home.html', context={'products': products})





def gem_detail(request, category_slug, gem_slug):
    try:
        single_gem = Gem.objects.get(category__slug=category_slug, slug=gem_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=cart_id_session(request), gem=single_gem).exists()
    except Exception as e:
        raise e
    return render(request, "gem_detail.html", context={'single_gem': single_gem, 'in_cart': in_cart, })






def shop(request, category_slug=None):
    categories = None
    gems = None
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        gems = Gem.objects.filter(category=categories, is_available=True)
        gem_count = gems.count()

    else:
        gems = Gem.objects.all().filter(is_available=True)
        gem_count = gems.count()
    return render(request, "shop.html", context={"gems": gems, "gem_count": gem_count})



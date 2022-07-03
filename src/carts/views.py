from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse



from django.shortcuts import render, redirect, get_object_or_404
from store.models import Gem, Variation
from .models import CartItem, Cart
from django.contrib.auth.decorators import login_required


# -------Create Session---------

def cart_id_session(request):
    cart = request.session.session_key
    #cart_data =request.session.session_data
    if not cart:
        cart = request.session.create()
    return cart

# -----------------ADD CART---------------

def add_cart(request, gem_id):
    current_user = request.user
    gem = Gem.objects.get(id=gem_id) #get the product
    # IF THE USER IS AUTHENTICATED
    if current_user.is_authenticated:
        gem_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(gem=gem, variation_category__iexact=key, variation_value__iexact=value)
                    gem_variation.append(variation)
                except:
                    pass



        is_cart_item_exists = CartItem.objects.filter(gem=gem, user=current_user).exists()
        
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(gem=gem, user=current_user)
            # existing_variations -> database
            # current variation -> products_variation
            # item_id -> database
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if gem_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(gem_variation)
                item_id = id[index]
                item = CartItem.objects.get(gem=gem, id=item_id)
                item.quantity += 1
                item.save()

            else:
                item = CartItem.objects.create(gem=gem, quantity=1, user=current_user)
                if len(gem_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*gem_variation)
                item.save()

        else:
            print('is_cart_item_ does not exists')
            print(current_user)
            cart_item = CartItem.objects.create(gem=gem, quantity=1, user=current_user)
            if len(gem_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*gem_variation)
            cart_item.save()
        return redirect('cart')

    # IF THE USER IS NOT AUTHENTICATED
    
    else:
        gem_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(gem=gem, variation_category__iexact=key, variation_value__iexact=value)
                    gem_variation.append(variation)
                except:
                    pass


        try:
            cart = Cart.objects.get(cart_id=cart_id_session(request)) # get the cart using the cart_id present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = cart_id_session(request)
            )
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(gem=gem, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(gem=gem, cart=cart)
            # existing_variations -> database
            # current variation -> product_variation
            # item_id -> database
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            print(ex_var_list)

            if gem_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(gem_variation)
                item_id = id[index]
                item = CartItem.objects.get(gem=gem, id=item_id)
                item.quantity += 1
                item.save()

            else:
                item = CartItem.objects.create(gem=gem, quantity=1, cart=cart)
                if len(gem_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*gem_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                gem = gem,
                quantity = 1,
                cart = cart,
            )
            if len(gem_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*gem_variation)
            cart_item.save()
        return redirect('cart')


# -----------------REMOVE CART---------------


def remove_cart(request, gem_id, cart_item_id):

    gem = get_object_or_404(Gem, id=gem_id)
    
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(gem=gem, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=cart_id_session(request))
            cart_item = CartItem.objects.get(gem=gem, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

# -----------------REMOVE CART_ITEM---------------

def remove_cart_item(request, gem_id, cart_item_id):
    gem = get_object_or_404(Gem, id=gem_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(gem=gem, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=cart_id_session(request))
        cart_item = CartItem.objects.get(gem=gem, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

# -----------------CART---------------

def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=cart_id_session(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.gem.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass #just ignore

    return render(request, 'cart.html', context={
                                            'total': total,
                                            'quantity': quantity,
                                            'cart_items': cart_items,
                                            'tax': tax,
                                            'grand_total': grand_total,
                                            })


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=cart_id_session(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.gem.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass #just ignore
    return render(request, 'checkout.html', context={
                                            'total': total,
                                            'quantity': quantity,
                                            'cart_items': cart_items,
                                            'tax': tax,
                                            'grand_total': grand_total,
                                            })




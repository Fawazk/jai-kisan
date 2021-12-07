
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from cart.models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from orders.forms import AddressForm, OrderForm
from orders.models import Address
from store.models import Product, Variation
from django.views.decorators.cache import never_cache

from django.contrib import auth, messages


# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)  # get the product
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key,variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

    
        is_cart_item_exists = CartItem.objects.filter(product=product,user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation)) 
                id.append(item.id)

            if product_variation in ex_var_list:
                # increasing cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product,quantity=1,user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                # cart_item.quantity += 1  # cart_item.quantity = cart_item.quantity+1
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=current_user,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')
        
    else:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key,variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass
        try:
            # get the cart using the cart_id present in the session
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()
        
        is_cart_item_exists = CartItem.objects.filter(product=product,cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))  
                id.append(item.id)

            if product_variation in ex_var_list:
                # increasing cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product,quantity=1,cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                # cart_item.quantity += 1  # cart_item.quantity = cart_item.quantity+1
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user,id=cart_item_id)
        else: 
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart,id=cart_item_id)
        if cart_item.quantity > 1:

            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user,id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart,id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

def cart(request, total=0, quantity=0, cart_items=None):
    try:
        if 'direct_order' in request.session:
            del request.session['direct_order']
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.get_price()* cart_item.quantity)
            quantity += cart_item.quantity
            tax = (cart_item.product.tax * total)/100
        grand_total = tax + total
    except ObjectDoesNotExist:
        pass
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        # 'variations':variations,
    }
    return render(request, 'store/cart.html', context)

@never_cache
@login_required(login_url='signin')
def checkout(request, total=0, quantity=0, cart_items=None):
    user=request.user
    form = AddressForm()
    address = Address.objects.filter(user=user)
    try:
        tax = 0
        grand_total = 0
        quantity=0
        item=None
        if request.user.is_authenticated:
            if 'direct_order' in request.session:
                product_id=request.session['direct_order']
                item=Product.objects.get(id=product_id)
            else:
                cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        if 'direct_order' in request.session:
            product_id=request.session['direct_order']
            item=Product.objects.get(id=product_id)
            tax=(2*item.get_price())/100
            total=item.get_price()
            quantity=1
            grand_total=total+tax
        else:
            for cart_item in cart_items:
                total += (cart_item.product.get_price() * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (3 * total)/100
            grand_total = tax + total
    except ObjectDoesNotExist:
        pass
    if request.session.has_key('coupon_id'):
        couponid=request.session['coupon_id']
        request.session['couponid']=couponid
        del request.session['coupon_id']
        coupen_discount= request.session['coupon_discount']
        coupen_discount_price = total*(coupen_discount)/100
        grand_total=grand_total-coupen_discount_price
    else:
        coupen_discount_price = 0
    request.session['grand_total']=grand_total  
    context = {
        'item':item,
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'coupen_discount_price':coupen_discount_price,
        'tax': tax,
        'grand_total': grand_total,
        'form':form,
        'address':address,
    }
    return render(request, 'store/checkout.html',context)

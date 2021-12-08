from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache
from cart.models import CartItem
from offer.models import Coupon, RedeemedCoupon
from .forms import OrderForm
import datetime
from .models import Order, OrderProduct,Payment
import json
from django.http import HttpResponse, JsonResponse
from store.models import Product
from django.conf import settings
from forex_python.converter import CurrencyRates
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
# from django.shortcuts import render, redirect
# from cart.models import CartItem
# from .forms import OrderForm
# import datetime
# from .models import Order, Payment, OrderProduct
# from django.core.mail import EmailMessage
# from django.template.loader import render_to_string
# Create your views here.

def dollar_rate():
    c = CurrencyRates()
    rate = c.get_rate('USD', 'INR')
    return rate

def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])


    # Store transaction details inside Payment model
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = 'paypal',
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # Move the cart items to Order Product table
    if 'direct_order' in request.session:
        print('fawaz paypal')
        product_id=request.session['direct_order']
        direct_item=Product.objects.get(id=product_id)
        payment_amount=direct_item.product.get_price()
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.user_id = request.user.id
        orderproduct.product_id = product_id
        orderproduct.quantity = 1
        orderproduct.product_price = payment_amount
        orderproduct.ordered = True
        orderproduct.save()
        
        product = Product.objects.get(id=product_id)
        product.stock -= 1
        product.save()
    else:
        cart_items = CartItem.objects.filter(user=request.user)
        for item in cart_items:
            payment_amount=item.quantity*item.product.get_price()
            orderproduct = OrderProduct()
            orderproduct.order_id = order.id
            orderproduct.payment = payment
            orderproduct.user_id = request.user.id
            orderproduct.product_id = item.product_id
            orderproduct.quantity = item.quantity
            orderproduct.product_price = payment_amount
            orderproduct.ordered = True
            orderproduct.save()

            cart_item = CartItem.objects.get(id=item.id)
            product_variation = cart_item.variations.all()
            orderproduct = OrderProduct.objects.get(id=orderproduct.id)
            orderproduct.variations.set(product_variation)
            orderproduct.save()


            # Reduce the quantity of the sold products
            product = Product.objects.get(id=item.product_id)
            product.stock -= item.quantity
            product.save()

    # Clear cart
    if 'direct_order' in request.session:
        del request.session['direct_order']
    else:
        CartItem.objects.filter(user=request.user).delete()
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)

def razorpay_payment_verification(request):
    order_number=request.session['order_number']
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=order_number)
    if request.method == 'POST':
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')

        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        request.session['razorpay_order_id']=razorpay_order_id
        try:
            razorpay_client.utility.verify_payment_signature(params_dict)
        except:
            return JsonResponse({'messages': 'error'})
    # Store transaction details inside Payment model
        payment = Payment(
            user = request.user,
            payment_id = razorpay_order_id,
            payment_method = 'rezorpay',
            amount_paid = order.order_total,
            status ='Completed',
        )
        payment.save()

        order.payment = payment
        order.is_ordered = True
        order.save()

    # Move the cart items to Order Product table
    if 'direct_order' in request.session:
        product_id=request.session['direct_order']
        direct_item=Product.objects.get(id=product_id)
        payment_amount=direct_item.product.get_price()
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.user_id = request.user.id
        orderproduct.product_id = product_id
        orderproduct.quantity = 1
        orderproduct.product_price = payment_amount
        orderproduct.ordered = True
        orderproduct.save()
        
        product = Product.objects.get(id=product_id)
        product.stock -= 1
        product.save()
    else:
        cart_items = CartItem.objects.filter(user=request.user)
        for item in cart_items:
            payment_amount=item.quantity*item.product.get_price()
            orderproduct = OrderProduct()
            orderproduct.order_id = order.id
            orderproduct.payment = payment
            orderproduct.user_id = request.user.id
            orderproduct.product_id = item.product_id
            orderproduct.quantity = item.quantity
            orderproduct.product_price = payment_amount
            orderproduct.ordered = True
            orderproduct.save()

            cart_item = CartItem.objects.get(id=item.id)
            product_variation = cart_item.variations.all()
            orderproduct = OrderProduct.objects.get(id=orderproduct.id)
            orderproduct.variations.set(product_variation)
            orderproduct.save()


        # Reduce the quantity of the sold products
            product = Product.objects.get(id=item.product_id)
            product.stock -= item.quantity
            product.save()

    # # Clear cart/session of buy now
    if 'direct_order' in request.session:
        del request.session['direct_order']
    else:
        CartItem.objects.filter(user=request.user).delete()
    return JsonResponse({'message': 'success'})

def payment_failed(request):
    return render(request,'payment_failed.html')


@never_cache
def place_order(request, total=0, quantity=0):
    current_user = request.user
    item=None
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if request.session.has_key('couponid'):
        couponid=request.session['couponid']
        coupon=Coupon.objects.get(id=couponid)
        if coupon.is_active==True:
            coupon_redeem=RedeemedCoupon()
            coupon_redeem.user=current_user
            coupon_redeem.coupon=coupon
            coupon_redeem.save()
    grand_total = 0
    tax = 0
    total_savings=0
    offer_savings=0
    if 'direct_order' in request.session:
        product=request.session['direct_order']
        item=Product.objects.get(id=product)
        tax=(2*item.get_price())/100
        total=item.get_price()
        quantity=1
        offer_savings=total-item.price
        grand_total=total+tax
        if request.session.has_key('couponid'):
            coupen_discount= request.session['coupon_discount']
            del request.session['couponid']
            coupen_discount_price = total*(coupen_discount)/100
            grand_total=grand_total-coupen_discount_price
            total_savings= grand_total-offer_savings
        else:
            coupen_discount_price=0    
    else:
        for cart_item in cart_items:
            total += (cart_item.product.get_price() * cart_item.quantity)
            offer_savings=total-(cart_item.product.price*cart_item.quantity)
            quantity += cart_item.quantity
            total_savings= grand_total-offer_savings
        tax = (2*total)/100
        grand_total = total+tax
        if request.session.has_key('couponid'):
            coupen_discount= request.session['coupon_discount']
            del request.session['couponid']
            coupen_discount_price = total*(coupen_discount)/100
            grand_total=grand_total-coupen_discount_price
            total_savings= grand_total-(coupen_discount_price-offer_savings)
        else:
            coupen_discount_price=0
    paypal_amount = grand_total/dollar_rate()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # store all billing information inside order table
            data = Order()
            data.user = current_user
            data.name = form.cleaned_data['name']
            data.phone = form.cleaned_data['phone']
            data.address = form.cleaned_data['address']
            data.locality = form.cleaned_data['locality']
            data.landmark = form.cleaned_data['landmark']
            data.city = form.cleaned_data['city']
            data.state = form.cleaned_data['state']
            data.pincode = form.cleaned_data['pincode']
            data.alternate_phone = form.cleaned_data['alternate_phone']
            data.order_total = grand_total
            data.tax = tax
            data.save()                      
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            request.session['order_number']=order_number
            request.session['grand_total']=grand_total
            order_amount = (grand_total*100)
            order_currency = 'INR'
            razorpay_order = razorpay_client.order.create(dict(amount=int(order_amount),currency=order_currency,payment_capture='0'))
            payment_order_id = razorpay_order['id']
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'item':item,
                'cart_items': cart_items,
                'total': round(total),
                'tax': round(tax,2),
                'quantity':quantity,
                'grand_total': grand_total,
                'paypal_amount':round(paypal_amount,2),
                'payment_order_id':payment_order_id,
                'total_savings':total_savings,
                'coupen_discount_price':coupen_discount_price,
                'razorpay_merchant_key':settings.RAZOR_KEY_ID,
                'razorpay_amount':order_amount,
                'currency': order_currency,
            }
            return render(request, 'orders/payments.html', context)
    return redirect('checkout')

def order_complete(request):
    order_number = request.session['order_number']
    del request.session['order_number']
    transID = request.GET.get('payment_id')
    try:
        order = Order.objects.get(is_ordered=False,order_number=order_number)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        order.is_ordered=True
        order.save()
        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity
        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'subtotal': subtotal,
        }
        return render(request, 'orders/order_complete.html', context)
    except Exception as e:
        print(e)
        try:
            order = Order.objects.get(order_number=order_number, is_ordered=True)
            ordered_products = OrderProduct.objects.filter(order_id=order.id)
            subtotal = 0
            for i in ordered_products:
                subtotal += i.product_price * i.quantity

            payment = Payment.objects.get(payment_id=transID)

            context = {
                'order': order,
                'ordered_products': ordered_products,
                'order_number': order.order_number,
                'transID': payment.payment_id,
                'payment': payment,
                'subtotal': subtotal,
            }
            return render(request, 'orders/order_complete.html', context)
        except:
            try:
                order = Order.objects.get(order_number=order_number, is_ordered=True)
                ordered_products = OrderProduct.objects.filter(order_id=order.id)

                subtotal = 0
                for i in ordered_products:
                    subtotal += i.product_price * i.quantity
                razorpay_order_id=request.session['razorpay_order_id']
                payment = Payment.objects.get(payment_id=razorpay_order_id)

                context = {
                    'order': order,
                    'ordered_products': ordered_products,
                    'order_number': order.order_number,
                    'transID': payment.payment_id,
                    'payment': payment,
                    'subtotal': subtotal,
                }
                return render(request, 'orders/order_complete.html', context)
            except (Order.DoesNotExist):
                return redirect('home')
        

def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True)
    orderproduct = OrderProduct.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders,
        'orderproduct':orderproduct,
    }
    return render(request, 'accounts/my_orders.html', context)
def orderdetails(request,order_id):
    orderproduct = OrderProduct.objects.get(id=order_id)
    context = {
        'orderproduct':orderproduct,
    }
    return render(request,'accounts/orderdetails.html',context)

def cancel_order(request,order_id):
    orders = Order.objects.get(id=order_id,user=request.user)
    orderproduct = OrderProduct.objects.get(user=request.user,order=orders)
    item_id=orderproduct.product.id
    product = Product.objects.get(id=item_id)
    print(product)
    product.stock += orderproduct.quantity
    print(product.stock)
    orderproduct.status = 0
    orderproduct.save()
    product.save()
    
    return redirect('my_orders')

def cash_on_delivery(request,total=0, quantity=0):
    # Move the cart items to Order Product table
    order_number = request.session['order_number']
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=order_number)
    if 'direct_order' in request.session:
        product_id=request.session['direct_order']
        direct_item=Product.objects.get(id=product_id)
        payment_amount=direct_item.get_price()
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.user_id = request.user.id
        orderproduct.product_id = product_id
        orderproduct.quantity = 1
        orderproduct.product_price = payment_amount
        orderproduct.ordered = True
        orderproduct.save()
        
        product = Product.objects.get(id=product_id)
        product.stock -= 1
        product.save()
    else:
        cart_items = CartItem.objects.filter(user=request.user)
        for item in cart_items:
            payment_amount=item.quantity*item.product.get_price()
            orderproduct = OrderProduct()
            orderproduct.order_id = order.id
            orderproduct.user_id = request.user.id
            orderproduct.product_id = item.product_id
            orderproduct.quantity = item.quantity
            orderproduct.product_price = payment_amount
            orderproduct.ordered = True
            orderproduct.save()


            cart_item = CartItem.objects.get(id=item.id)
            product_variation = cart_item.variations.all()
            orderproduct = OrderProduct.objects.get(id=orderproduct.id)
            orderproduct.variations.set(product_variation)
            orderproduct.save()


        #   # Reduce the quantity of the sold products
            product = Product.objects.get(id=item.product_id)
            product.stock -= item.quantity
            product.save()

    # # Clear cart
    if 'direct_order' in request.session:
        del request.session['direct_order']
    else:
        CartItem.objects.filter(user=request.user).delete()
    return redirect('order_complete')

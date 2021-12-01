from django.shortcuts import redirect, render
from cart.models import CartItem
from .forms import OrderForm
import datetime
from .models import Order, OrderProduct,Payment
import json
from django.http import HttpResponse, JsonResponse
from store.models import Product
from django.conf import settings
from forex_python.converter import CurrencyRates
# import razorpay
# client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
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
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # Move the cart items to Order Product table
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()


    #     # Reduce the quantity of the sold products
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # # Clear cart
    CartItem.objects.filter(user=request.user).delete()

    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)

def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    grand_total = 0
    tax = 0
    print("hekkk")
    if 'direct_order' in request.session:
        product=request.session['direct_order']
        item=Product.objects.get(id=product)
        tax=(2*item.get_price())/100
        total=item.get_price()
        grand_total=total+tax  
        del request.session['direct_order']
    else:
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2*total)/100
        grand_total = total+tax
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
            order = Order.objects.get(
                user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
                'paypal_amount':round(paypal_amount,2),
            }
            return render(request, 'orders/payments.html', context)
    return redirect('checkout')

def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

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
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')

def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('created_at')
    orderproduct = OrderProduct.objects.filter(user=request.user)
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

from .models import Banner
from orders.forms import AddressForm
from orders.models import Address, Order, OrderProduct
from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from accounts.models import Account
from cart.models import Cart, CartItem
from store.models import Product, Variation
from .form import RegisterationForm, edit_profileForm
from django.contrib import auth, messages
from .otp_verify import otpverify, verify
from django.contrib.auth import logout
from cart.views import _cart_id
# Create your views here.


def home(request):
    products = Product.objects.all().filter(is_available=True)
    banner = Banner.objects.all()
    context = {
        'products': products,
        'banner':banner,
    }
    print(context)
    return render(request, 'index.html', context)


def register(request):
    global phone_number,user
    if request.user.is_authenticated:
        return redirect('home')
    form = RegisterationForm()
    if request.method == 'POST':
        form = RegisterationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = str(first_name+last_name)
            request.session['key']=phone_number
            user = Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            otpverify(phone_number)
            return redirect('confirm_register_otp')
    context ={
        'form':form
    }
    return render(request,'register.html',context)
def resent_register_otp(request):
    phone_number=request.session['key']
    otpverify(phone_number)
    return redirect('confirm_register_otp')

def confirm_register_otp(request): 
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        otp1 = request.POST['otp1']
        otp2 = request.POST['otp2']
        otp3 = request.POST['otp3']
        otp4 = request.POST['otp4']
        otp5 = request.POST['otp5']
        otp6 = request.POST['otp6']
        otp = [otp1+otp2+otp3+otp4+otp5+otp6]
        print(otp)
        if verify(phone_number,otp):
            user.phone_number=phone_number
            user.save()
            messages.success(request,'Registered successfully')
            return redirect('signin')
        else:
            print('OTP not matching')
            return redirect('confirm_register_otp')
    return render(request,'confirm_register_otp.html')


def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item =CartItem.objects.filter(cart=cart)
                    product_variation = []
                    for item in cart_item:
                        variation = item. variations.all()
                        product_variation.append(list(variation))
                    cart_item = CartItem.objects.filter(user=user)   
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))  
                        id.append(item.id)
                        
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            print(index)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            print(item.quantity)
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('signin')
    return render(request, 'signin.html')


def forgot_password(request):
    global mobile_number
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        mobile_number = request.POST['mobile']
        print(mobile_number)
        if Account.objects.filter(phone_number=mobile_number).exists():
            print('----------------')
            otpverify(mobile_number)
            request.session['keys'] = mobile_number
            return redirect('otp')
        else:
            messages.error(request, 'Phone number is not matching!!!')
            return redirect('forgot_password')
    return render(request, 'password_otp_login.html')
def resent_otp(request):
    phone_number=request.session['keys']
    otpverify(phone_number)
    return redirect('otp')

def otp(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        otp1 = request.POST['otp1']
        otp2 = request.POST['otp2']
        otp3 = request.POST['otp3']
        otp4 = request.POST['otp4']
        otp5 = request.POST['otp5']
        otp6 = request.POST['otp6']
        otp = [otp1+otp2+otp3+otp4+otp5+otp6]
        phone_number=request.session['keys']
        if verify(phone_number, otp):
            print(otp)
            return redirect('new_password')
        else:
            print('OTP not matching')
            return redirect('otp')
    return render(request, 'confirm_password_otp.html')


def new_password(request):
    print('________________________')
    if 'keys' not in request.session:
        return redirect('signin')
    else:
        number = request.session['keys']
        print(number+'-----------------')
        if request.method == 'POST':
            password = request.POST['password1']
            password2 = request.POST['password2']

            if password == password2:
                user = Account.objects.get(phone_number=number)
                user.set_password(password)
                user.save()
                messages.error(request, 'Password changed successfully ')
                return redirect('signin')
            else:
                messages.error(request, 'Password is not matching!!!')
                return redirect('new_password')
        return render(request, 'new_password.html')

@login_required(login_url='signin')
def profile(request):
    account = Account.objects.get(id=request.user.id)
    print(account)
    context ={
        'account':account,
    }
    return render(request,'accounts/account.html',context)


def edit_profile(request,id):
    form = edit_profileForm(request.POST)
    list_user = Account.objects.get(id=id)
    form = edit_profileForm(instance=list_user)
    if request.method=='POST':
        form=edit_profileForm(request.POST,request.FILES,instance=list_user)
        if form.is_valid():
            try:
                form.save()                
            except:
                context = {'form':form}
                return render(request,'accounts/edit_profile.html',context)
            return redirect('profile')
    context = {'form':form}
    return render(request,'accounts/edit_profile.html',context)
def change_password(request):
    curr_user=request.user
    user_email =curr_user.email
    print(user_email)

    if request.method == 'POST':
        current_password= request.POST['current_password']
        print(current_password)
        password = request.POST['password']
        password2 = request.POST['password2']
        user = auth.authenticate(email=user_email,password=current_password)
        print(user)
        if user is not None:
            if password == password2:
                print(password)
                user.set_password(password)
                user.save()
                auth.login(request, user)
                return redirect('profile')
            else:
                print('++++++++++')
                messages.error(request, 'Password is not matching!!!')
                return render(request, 'accounts/change_password.html')
        else:
            print('___________-')
            messages.error(request, 'Current password is not matching!!!')
            return render(request, 'accounts/change_password.html')
    return render(request, 'accounts/change_password.html')


def address_management(request):
    user=request.user
    form = AddressForm()
    orders = Address.objects.filter(user=user)
    context ={
        'orders':orders,
        'form':form,
    }
    return render(request,'accounts/address_management.html',context)
def edit_address(request,id):
    url = request.META.get('HTTP_REFERER')
    address = Address.objects.get(id=id)    
    form = AddressForm(instance=address)
    if request.method=='POST':
        form = AddressForm(request.POST, request.FILES, instance=address)
        print(form)
        if form.is_valid():
            try:
                form.save()                
            except:
                context = {
                    'form':form
                    }
                return render(request,'accounts/edit_address.html',context)
            return redirect(url)
    context = {
        'form':form,
        }
    return render(request,'accounts/edit_address.html',context)


def cancel_address(request,id):
    address = Address.objects.get(id=id,user=request.user)
    address.delete()
    return redirect('address_management')

def add_address(request):
    form = AddressForm()
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address=form.save(commit=False)
            address.user=request.user
            address.save()
            return redirect('address_management')
    context ={
        'form':form,
    }
    return render(request,'accounts/address_management.html',context)

def buynow(request):
    return redirect('check')

def logout(request):
    auth.logout(request)
    return redirect('signin')

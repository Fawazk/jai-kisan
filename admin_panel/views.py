from django.shortcuts import render,redirect
from accounts.models import Account
from category.form import CategoryForm
from category.models import category
from offer.form import CategoryOfferForm, ProductOfferForm
from offer.models import CategoryOffer, ProductOffer
from orders.forms import OrderProductForm
from orders.models import Order, OrderProduct
from store.models import Product
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from store.form import ProductForm
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.


@staff_member_required
def admin_dashboard(request):
    return render(request,'adminpanel/index.html')

def adminpanel(request):
    print('rtyuiop')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user=auth.authenticate(email=email, password=password,is_superuser=True)
        if user is not None:
            auth.login(request,user)
            return redirect('admin_dashboard')
        else:
            messages.error(request,'Invalid credentials')
            return redirect('adminpanel')
    return render(request,'adminpanel/login.html')
@staff_member_required
def category_list(request):
    categories = category.objects.all()
    context ={
        'categories': categories,
    }
    return render(request,'adminpanel/category_list.html',context)
@staff_member_required
def deletecategory(request,cat_id):
    categories = category.objects.get(id=cat_id)
    categories.delete()
    return redirect('category_list')


@staff_member_required
def editcategory(request,cat_id):
    list_cats = category.objects.get(id=cat_id)
    form = CategoryForm(instance=list_cats)
    if request.method=='POST':
        form=CategoryForm(request.POST,request.FILES,instance=list_cats)
        if form.is_valid():
            try:
                form.save()                
            except:
                context = {'form':form}
                return render(request,'adminpanel/edit_category.html',context)
            return redirect('category_list')
    context = {'form':form}  
    return render(request,'adminpanel/edit_category.html',context)
    
@staff_member_required
def addcategory(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST,request.FILES)

        if form.is_valid():
            category=form.save(commit=False)
            category.slug=category.category_name.lower().replace("","-")
            category.save()
            return redirect('category_list')
    context = {
            'form':form
        } 
    return render(request,'adminpanel/add_category.html',context)   
    
@staff_member_required
def Product_list(request):
    products = Product.objects.all()
    context ={
        'products': products,
    }
    return render(request,'adminpanel/Product_list.html',context)

@staff_member_required
def deleteproduct(request,cat_id):
    products = Product.objects.get(id=cat_id)
    products.delete()
    return redirect('Product_list')
@staff_member_required
def addProduct(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)

        if form.is_valid():
            product=form.save(commit=False)
            product.slug=product.product_name.lower().replace(" ","-")
            product.save()
            return redirect('Product_list')
    context = {
            'form':form
        }
    return render(request,'adminpanel/add_product.html',context) 
@staff_member_required
def editproduct(request,cat_id):
        list_cats = Product.objects.get(id=cat_id)
        form = ProductForm(instance=list_cats)
        if request.method=='POST':
            form=ProductForm(request.POST,request.FILES,instance=list_cats)
            if form.is_valid():
                try:
                    form.save()                
                except:
                    context = {'form':form}
                    return render(request,'adminpanel/editproduct.html',context)
                return redirect('Product_list')

        context = {'form':form}  
        return render(request,'adminpanel/editproduct.html',context)
    
    
def user_list(request):
    user = Account.objects.all()
    context ={
        'user': user,
    }
    return render(request,'adminpanel/user_management.html',context)

def deleteuser(request,user_id):
    products = Account.objects.get(id=user_id)
    products.delete()
    return redirect('user_list')


def blockuser(request,user_id):
    user = Account.objects.get(id=user_id)
    user.is_active = False
    user.save()
    return redirect('user_list')

def unblockuser(request,user_id):
    user = Account.objects.get(id=user_id)
    user.is_active = True
    user.save()
    return redirect('user_list')



def order_list(request):
    order_list = OrderProduct.objects.all()
    context = {
        'order_list':order_list,
    }
    return render(request,'adminpanel/order_list.html',context)

def order_edit(request,order_product_id):
    list_order = OrderProduct.objects.get(id=order_product_id)
    form = OrderProductForm(instance=list_order)
    if request.method == 'POST':
        form=OrderProductForm(request.POST,request.FILES,instance=list_order)
        if form.is_valid():
            try:
                form.save()                
            except:
                context = {'form':form}
                return render(request,'adminpanel/order_edit.html',context)
            return redirect('order_list')
    context = {'form':form}     
    return render(request,'adminpanel/order_edit.html',context)

def order_history(request):
    order_history = OrderProduct.objects.all()
    context = {
        'order_history':order_history,
    }
    return render(request,'adminpanel/order_history.html',context)

def product_offer(request):
    productoffer=ProductOffer.objects.all()
    context={
        'productoffer':productoffer,
    }
    return render(request,'adminpanel/product_offer.html',context)
def deleteproductoffer(request,offer_id):
    productoffer=ProductOffer.objects.get(id=offer_id)
    productoffer.delete()
    return redirect('product_offer')

def editproductoffer(request,offer_id):
    list_order_product=ProductOffer.objects.get(id=offer_id)
    form = ProductOfferForm(instance=list_order_product)
    if request.method == 'POST':
        form = ProductOfferForm(request.POST,request.FILES,instance=list_order_product)
        print(form)
        if form.is_valid():
            try:
                form.save()
            except:
                context = {'form':form}
                return render(request,'adminpanel/editoffer.html',context)
            return redirect('product_offer')
    context = {'form':form}     
    return render(request,'adminpanel/editoffer.html',context)

def category_offer(request):
    category_offer = CategoryOffer.objects.all()
    context ={
        'category_offer':category_offer,
    }
    return render(request,'adminpanel/category_offer.html',context)

def deletecategoryoffer(request,offer_id):
    category_list=CategoryOffer.objects.get(id=offer_id)
    category_list.delete()
    return redirect('category_offer')


def editcategoryoffer(request,offer_id):
    category = CategoryOffer.objects.get(id=offer_id)
    form = CategoryOfferForm(instance=category)
    if request.method == 'POST':
        form = CategoryOfferForm(request.POST,request.FILES,instance=category)
        if form.is_valid():
            try:
                form.save()
            except:
                context = {'form':form}
                return render(request,'adminpanel/editcategoryoffer.html',context)
            return redirect('category_offer')
    context = {'form':form}
    return render(request,'adminpanel/editcategoryoffer.html',context)


def add_productoffer(request):
    form = ProductOfferForm()
    if request.method == 'POST':
        form = ProductOfferForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_offer')
    context = {
            'form':form,
    }
    return render(request,'adminpanel/add_productoffer.html',context)

def add_categoryoffer(request):
    form = CategoryOfferForm()
    if request.method == 'POST':
        form = CategoryOfferForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_offer')
    context = {
            'form':form,
    }
    return render(request,'adminpanel/add_categoryoffer.html',context)
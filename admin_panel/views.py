from django.shortcuts import render,redirect
from accounts.models import Account
from category.models import category
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
    print(list_cats)
    context = { 'list_cats' : list_cats }
    if request.method == 'POST':
        category_Name         = request.POST['category_Name']
        category_slug         = request.POST['category_slug']
        category_Description  = request.POST['category_Description']
        
        list_cats.category_name  = category_Name
        list_cats.slug           = category_slug
        list_cats.description    = category_Description
        list_cats.save()
        return redirect('category_list')
    return render(request,'adminpanel/edit_category.html',context)
    
@staff_member_required
def addcategory(request):
    if request.method=='POST':
        category_Name = request.POST['category_Name']
        category_slug         = request.POST['category_slug']
        category_Description  = request.POST['category_Description']
        if category.objects.filter(category_name=category_Name).exists():
            messages.info(request,'Category name taken')
            return redirect('addcategory')
        else:
            added_cat = category.objects.create(category_name=category_Name,slug=category_slug,description=category_Description)
            added_cat.save()
            return redirect('category_list')
        
    return render(request,'adminpanel/add_category.html')   
    
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
            form.save()
            return redirect('Product_list')
    context = {
            'form':form
        }
    return render(request,'adminpanel/add_product.html',context) 


# @staff_member_required
# def editproduct(request,cat_id):
#     list_cats = Product.objects.get(id=cat_id)
#     form = ProductForm(instance=list_cats)
#     print(list_cats)
#     context = { 'list_cats' : list_cats }
#     if request.method == 'POST':
        
#         list_cats.save()
#         return redirect('Product_list')
#     return render(request,'adminpanel/editproduct.html',context)



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
    return redirect('user_management')


def blockuser(request,user_id):
    user = Account.objects.get(id=user_id)
    user.is_active = False
    user.save()
    return redirect('user_management')

def unblockuser(request,user_id):
    user = Account.objects.get(id=user_id)
    user.is_active = True
    user.save()
    return redirect('user_management')



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
    



    
